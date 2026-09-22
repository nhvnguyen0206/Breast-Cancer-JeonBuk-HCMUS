"""Read-only FIT diagnostic at the shared exam representation (eval mode)."""
import argparse
import json
import random
import numpy as np
import torch
from torch.nn import functional as F
from tn_mammo.data import FourViewDataset
from tn_mammo.engine import load_model
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.sampling import training_sampler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--train-batches', type=int, default=0)
    parser.add_argument('--shared-fusion', action='store_true')
    args = parser.parse_args()
    torch.manual_seed(42)
    random.seed(42)
    np.random.seed(42)
    assert '5090' in torch.cuda.get_device_name(0)
    model, cfg = load_model(args.checkpoint, torch.device('cuda'))
    model.train(bool(args.train_batches))
    if args.shared_fusion:
        model.features.requires_grad_(False)
    ds = FourViewDataset(args.manifest, cfg['image_size'], training=bool(args.train_batches),
                         input_mode=cfg['input_mode'], resize_mode=cfg['resize_mode'],
                         augmentation=cfg.get('augmentation'))
    counts = np.bincount(ds.labels, minlength=4)
    loss = MultiTaskLoss(counts, **cfg['loss']).cuda()
    assert not cfg['loss'].get('label_smoothing', 0) and cfg['loss'].get('focal_scale', 1) == 1
    assert cfg['loss'].get('focal_normalization', 'class_mean') == 'class_mean'
    assert cfg['loss'].get('binary_normalization', 'batch_weight_mean') == 'batch_weight_mean'
    captured = []
    hook = model.exam_norm.register_forward_hook(lambda m, i, o: captured.append(o if args.shared_fusion else o.detach()))
    rng = np.random.default_rng(42)
    results = []
    batches = []
    for label in range(4):
        indices = np.flatnonzero(ds.labels == label)
        indices = rng.choice(indices, size=min(16, len(indices)), replace=False)
        batches.extend([[int(index)] for index in indices])
    if args.train_batches:
        sampler, _ = training_sampler(ds.labels, cfg['training'].get('sampling_power', 0), 42)
        indices = list(sampler) if sampler is not None else torch.randperm(len(ds)).tolist()
        batches = [indices[i:i+2] for i in range(0, min(len(indices)-1, args.train_batches*2), 2)]
    for indices in batches:
            with torch.set_grad_enabled(args.shared_fusion):
                model(torch.stack([ds[index]['views'] for index in indices]).cuda())
            exam = captured.pop().requires_grad_(True)
            logits = model.flat_head(exam).float()
            probs = logits.softmax(1)
            y = torch.tensor([int(ds.labels[index]) for index in indices], device='cuda')
            terms = {
                'focal': ((1-probs.gather(1,y[:,None]).squeeze(1))**loss.gamma * F.cross_entropy(logits,y,weight=loss.weights,reduction='none')).mean(),
                'ordinal': loss.ordinal * F.binary_cross_entropy_with_logits(model.ordinal_score(exam)+model.ordinal_bias, (y[:,None]>torch.arange(3,device='cuda')).float(),reduction='none').sum(1).mean(),
                'binary': loss.binary * F.cross_entropy(model.binary_head(exam), (y>=2).long(),weight=loss.binary_weights),
                'neighbor': loss.neighbor * (probs*loss.cost[y]).sum(1).mean(),
            }
            target = model.bilateral[-1].weight if args.shared_fusion else exam
            grads = {k:torch.autograd.grad(v,target,retain_graph=True)[0].flatten() for k,v in terms.items()}
            results.append({'labels':y.tolist(),'norms':{k:g.norm().item() for k,g in grads.items()},
                            'cosine_to_focal':{k:F.cosine_similarity(g[None],grads['focal'][None]).item() for k,g in grads.items()}})
    hook.remove()
    print(json.dumps({'mode': 'train, augmented sampled batches, FP32' if args.train_batches else 'eval, unaugmented single cases',
                      'scope':('bilateral final linear weight' if args.shared_fusion else 'exam feature') + '; no optimizer/checkpoint writes; BN changes in memory only',
                      'counts':counts.tolist(),'records':results}))


if __name__ == '__main__':
    main()
