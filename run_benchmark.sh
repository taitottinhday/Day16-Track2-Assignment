#!/usr/bin/env bash
# Run this on the cloud VM from ~/ml-benchmark after Kaggle download has finished.
set -euo pipefail

WORK_DIR="${WORK_DIR:-$HOME/ml-benchmark}"
DATA_FILE="$WORK_DIR/creditcard.csv"

cd "$WORK_DIR"
python3 -c "import lightgbm, sklearn, pandas, numpy; print('BOOTSTRAP_OK')"

if [[ ! -f "$DATA_FILE" ]]; then
  echo "Missing $DATA_FILE." >&2
  echo "Download the required Kaggle dataset first:" >&2
  echo "kaggle datasets download -d mlg-ulb/creditcardfraud --unzip -p $WORK_DIR/" >&2
  exit 1
fi

python3 benchmark.py \
  --data "$DATA_FILE" \
  --cloud "${CLOUD:-gcp}" \
  --instance-type "${INSTANCE_TYPE:-e2-medium}" \
  --output benchmark_result.json | tee benchmark_terminal_output.txt

python3 -m json.tool benchmark_result.json
