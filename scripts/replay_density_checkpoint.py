"""Recompute completed-run predictions from images; never alter the source run."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd


def compare_predictions(saved, replayed):
    for frame in (saved, replayed):
        if frame.empty or frame.case_id.duplicated().any():
            raise ValueError('Empty or duplicate prediction IDs')
    if set(saved.case_id) != set(replayed.case_id):
        raise ValueError('Prediction membership mismatch')
    saved = saved.set_index('case_id').sort_index()
    replayed = replayed.set_index('case_id').sort_index()
    for column in ('true_index', 'pred_index', 'pred_label'):
        if not saved[column].equals(replayed[column]):
            raise ValueError('Prediction mismatch: ' + column)
    columns = ['prob_' + label for label in 'ABCD']
    a, b = saved[columns].to_numpy(float), replayed[columns].to_numpy(float)
    for probabilities in (a, b):
        if (not np.isfinite(probabilities).all()
                or np.any((probabilities < 0) | (probabilities > 1))
                or not np.allclose(probabilities.sum(1), 1, rtol=0, atol=1e-5)):
            raise ValueError('Invalid probabilities')
    if not np.allclose(a, b, rtol=1e-5, atol=1e-6):
        raise ValueError('Replayed probabilities differ from saved predictions')
    return {'samples': len(saved), 'max_probability_abs_error': float(np.abs(a-b).max()),
            'exact_predicted_labels': True, 'probability_rtol': 1e-5, 'probability_atol': 1e-6}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', required=True)
    parser.add_argument('--code-root', required=True, help='Immutable training snapshot')
    args = parser.parse_args()
    sys.path.insert(0, str(Path(args.code_root).resolve() / 'src'))
    import torch
    from torch.utils.data import DataLoader
    from tn_mammo.data import FourViewDataset
    from tn_mammo.engine import load_model, predict, metrics
    run = Path(args.run_dir)
    history = json.loads((run / 'history.json').read_text())
    if [r['epoch'] for r in history] != list(range(1, 51)):
        raise ValueError('Replay requires a completed50 run')
    gpu = torch.cuda.get_device_name(0)
    if '5090' not in gpu:
        raise ValueError('RTX5090 required')
    checkpoint_path = run / 'best.pt'
    digest = hashlib.sha256(checkpoint_path.read_bytes()).hexdigest()
    checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=True)
    selected = max(history, key=lambda r: r['valid']['macro_f1'])
    if checkpoint['epoch'] != selected['epoch']:
        raise ValueError('Wrong selected checkpoint')
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    model, config = load_model(checkpoint_path, torch.device('cuda'))
    dataset = FourViewDataset(checkpoint['valid_manifest'], config['image_size'],
                             input_mode=config.get('input_mode', 'dicom'),
                             resize_mode=config.get('resize_mode', 'stretch'))
    replayed = predict(model, DataLoader(dataset, shuffle=False, num_workers=0,
                        batch_size=int(config['training']['batch_size'])), torch.device('cuda'))
    saved = pd.read_csv(run / 'valid_predictions.csv', dtype={'case_id': str})
    result = compare_predictions(saved, replayed)
    measured = metrics(replayed.true_index, replayed.pred_index)
    for key, value in measured.items():
        expected = selected['valid'][key]
        if isinstance(value, float):
            matches = np.isclose(value, expected, rtol=1e-9, atol=1e-10)
        else:
            matches = value == expected
        if not matches:
            raise ValueError('Recomputed metric mismatch: ' + key)
    if hashlib.sha256(checkpoint_path.read_bytes()).hexdigest() != digest:
        raise ValueError('Checkpoint changed during replay')
    print(json.dumps({'replay': 'PASS', 'gpu': gpu, 'checkpoint_sha256': digest,
                      'architecture': checkpoint['architecture'],
                      'selected_epoch': checkpoint['epoch'], 'metrics': measured,
                      'independent_test': False, **result}, indent=2))


if __name__ == '__main__':
    main()
