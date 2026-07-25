# Queue, nohup và vận hành

## File code

```text
filecode1/scripts/run_queue.sh
```

Queue chạy tuần tự:

```text
baseline evaluation
  -> v2_224
  -> v2_384
  -> v2_512
  -> generate tonghop.pdf
```

`set -Eeuo pipefail` làm queue dừng nếu một bước trả exit code khác 0.
`queue_status.txt` ghi bước đang chạy, thời gian và trạng thái cuối.

Trạng thái hoàn tất hiện tại:

```text
COMPLETED report=/mnt/hcmus/breast_vn/code/new_implement_v2/tonghop.pdf
```

## Chạy queue bằng GPU 1

```bash
cd /mnt/hcmus/breast_vn/code/new_implement_v2
nohup setsid env CUDA_VISIBLE_DEVICES=1 \
  /bin/bash scripts/run_queue.sh \
  </dev/null >logs/queue.log 2>&1 &
```

Không chạy lại lệnh này nếu output cũ cần được bảo toàn mà chưa đổi tên folder
run, vì checkpoint/metrics/history có thể bị ghi tiếp hoặc thay thế.

## Theo dõi

```bash
cd /mnt/hcmus/breast_vn/code/new_implement_v2
tail -F \
  queue_status.txt \
  logs/queue.log \
  logs/baseline_selected_eval.log \
  logs/v2_224.log \
  logs/v2_384.log \
  logs/v2_512.log \
  logs/report.log
```

Kiểm tra GPU:

```bash
watch -n 5 nvidia-smi
```
