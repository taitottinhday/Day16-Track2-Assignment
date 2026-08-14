#!/bin/bash
set -euo pipefail

WORK_DIR="$HOME/ml-benchmark"
DATA_FILE="$WORK_DIR/creditcard.csv"
SCRIPT_DIR="/tmp"
mkdir -p "$WORK_DIR"
cp "$SCRIPT_DIR/benchmark.py" "$WORK_DIR/benchmark.py"
cd "$WORK_DIR"

python3 -c "import lightgbm, sklearn, pandas, numpy; print('BOOTSTRAP_OK')"

if [ ! -f "$DATA_FILE" ]; then
  echo "Downloading the ULB Credit Card Fraud dataset from OpenML..."
  python3 - <<'PY'
from pathlib import Path
from sklearn.datasets import fetch_openml

target = Path.home() / "ml-benchmark" / "creditcard.csv"
dataset = fetch_openml("creditcard", version=1, as_frame=True, parser="auto")
frame = dataset.frame.rename(columns={dataset.target.name: "Class"})
frame["Class"] = frame["Class"].astype(int)
frame.to_csv(target, index=False)
print(f"Saved {len(frame)} rows to {target}")
PY
fi

python3 benchmark.py \
  --data "$DATA_FILE" \
  --cloud gcp \
  --instance-type e2-medium \
  --output benchmark_result.json | tee benchmark_terminal_output.txt &
BENCHMARK_PID=$!

sleep 2
echo "--- RESOURCE SNAPSHOT DURING TRAINING ---" | tee resource_snapshot.txt
top -b -n 1 | head -n 20 | tee -a resource_snapshot.txt || true
free -h | tee -a resource_snapshot.txt
ip -s link | tee -a resource_snapshot.txt

wait "$BENCHMARK_PID"

python3 -m json.tool benchmark_result.json >/dev/null
