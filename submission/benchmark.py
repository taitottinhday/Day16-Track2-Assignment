#!/usr/bin/env python3
"""Run the Day 16 LightGBM CPU benchmark on Kaggle's creditcard.csv.

Run this script on the cloud VM after downloading the original Kaggle dataset
to ~/ml-benchmark/creditcard.csv. The test set is held out until the final
evaluation; early stopping uses the validation set only.
"""

from __future__ import annotations

import argparse
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split


SEED = 16


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("creditcard.csv"))
    parser.add_argument("--cloud", default="gcp")
    parser.add_argument("--instance-type", default="e2-medium")
    parser.add_argument("--output", type=Path, default=Path("benchmark_result.json"))
    return parser.parse_args()


def median_prediction_seconds(model: lgb.LGBMClassifier, data: pd.DataFrame, repeats: int) -> float:
    """Measure warm-cache prediction time; the warm-up belongs outside timing."""
    elapsed = []
    for _ in range(repeats):
        started = time.perf_counter()
        model.predict_proba(data)
        elapsed.append(time.perf_counter() - started)
    return float(np.median(elapsed))


def main() -> None:
    args = parse_args()
    data_path = args.data.expanduser()

    load_started = time.perf_counter()
    df = pd.read_csv(data_path)
    data_load_seconds = time.perf_counter() - load_started

    expected_rows, expected_columns = 284_807, 31
    if df.shape != (expected_rows, expected_columns) or "Class" not in df.columns:
        raise ValueError(
            "Expected Kaggle creditcard.csv with 284807 rows, 31 columns, and a 'Class' column; "
            f"got shape {df.shape}. Re-download mlg-ulb/creditcardfraud before benchmarking."
        )
    if int(df.isna().sum().sum()) != 0:
        raise ValueError("The original benchmark dataset must not contain missing values.")

    X, y = df.drop(columns="Class"), df["Class"].astype(int)
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )
    X_train, X_valid, y_train, y_valid = train_test_split(
        X_trainval, y_trainval, test_size=0.25, random_state=SEED, stratify=y_trainval
    )

    model = lgb.LGBMClassifier(
        n_estimators=300,
        learning_rate=0.05,
        random_state=SEED,
        n_jobs=2,
        verbosity=-1,
    )
    training_started = time.perf_counter()
    model.fit(
        X_train,
        y_train,
        eval_set=[(X_valid, y_valid)],
        eval_metric="auc",
        callbacks=[lgb.early_stopping(20, verbose=False)],
    )
    training_seconds = time.perf_counter() - training_started

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    one_row, batch = X_test.iloc[:1], X_test.iloc[:1000]
    model.predict_proba(one_row)  # Warm-up outside all timing.
    model.predict_proba(batch)
    single_seconds = median_prediction_seconds(model, one_row, repeats=50)
    batch_seconds = median_prediction_seconds(model, batch, repeats=10)

    result = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "cloud": args.cloud,
        "instance_type": args.instance_type,
        "architecture": platform.machine(),
        "versions": {
            "python": platform.python_version(),
            "lightgbm": lgb.__version__,
            "sklearn": sklearn.__version__,
            "pandas": pd.__version__,
            "numpy": np.__version__,
        },
        "dataset_rows": int(len(df)),
        "dataset_columns": int(df.shape[1]),
        "fraud_rows": int(y.sum()),
        "seed": SEED,
        "split": {"train": int(len(X_train)), "validation": int(len(X_valid)), "test": int(len(X_test))},
        "n_jobs": 2,
        "decision_threshold": 0.5,
        "data_load_seconds": data_load_seconds,
        "training_seconds": training_seconds,
        "best_iteration": int(model.best_iteration_),
        "auc_roc": float(roc_auc_score(y_test, probabilities)),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "latency_1_row_ms": single_seconds * 1_000,
        "latency_repeats": 50,
        "batch_rows": int(len(batch)),
        "batch_repeats": 10,
        "batch_1000_rows_seconds": batch_seconds,
        "throughput_1000_rows_per_second": len(batch) / batch_seconds,
        "timing_summary": "median; warm-up excluded; predict_proba on pandas input",
    }
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
