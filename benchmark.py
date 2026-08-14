#!/usr/bin/env python3
"""CPU LightGBM benchmark for the Day 16 credit-card fraud lab."""

from __future__ import annotations

import argparse
import json
import platform
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("creditcard.csv"))
    parser.add_argument("--cloud", default="gcp")
    parser.add_argument("--instance-type", default="e2-medium")
    parser.add_argument("--output", type=Path, default=Path("benchmark_result.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    load_started = time.perf_counter()
    data = pd.read_csv(args.data)
    load_time = time.perf_counter() - load_started

    if "Class" not in data.columns:
        raise ValueError("Dataset must contain the target column 'Class'.")

    features = data.drop(columns=["Class"])
    target = data["Class"].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=target,
    )

    parameters = {
        "n_estimators": 300,
        "learning_rate": 0.05,
        "num_leaves": 31,
        "class_weight": "balanced",
        "random_state": RANDOM_STATE,
        "n_jobs": -1,
        "verbosity": -1,
    }
    model = lgb.LGBMClassifier(**parameters)

    training_started = time.perf_counter()
    model.fit(x_train, y_train)
    training_time = time.perf_counter() - training_started

    fraud_probability = model.predict_proba(x_test)[:, 1]
    prediction = model.predict(x_test)
    tn, fp, fn, tp = confusion_matrix(y_test, prediction).ravel()

    one_row = x_test.iloc[[0]]
    model.predict_proba(one_row)  # Warm-up.
    latency_measurements_ms = []
    for _ in range(100):
        started = time.perf_counter()
        model.predict_proba(one_row)
        latency_measurements_ms.append((time.perf_counter() - started) * 1_000)

    batch = x_test.iloc[:1_000]
    model.predict_proba(batch)  # Warm-up.
    throughput_runs = 20
    started = time.perf_counter()
    for _ in range(throughput_runs):
        model.predict_proba(batch)
    batch_seconds = time.perf_counter() - started
    throughput = (len(batch) * throughput_runs) / batch_seconds

    best_iteration = getattr(model, "best_iteration_", None)
    if not best_iteration:
        best_iteration = None

    result = {
        "cloud": args.cloud,
        "instance_type": args.instance_type,
        "python_version": platform.python_version(),
        "random_state": RANDOM_STATE,
        "dataset_rows": int(len(data)),
        "dataset_features": int(features.shape[1]),
        "fraud_rows": int(target.sum()),
        "test_size": int(len(y_test)),
        "model": "LGBMClassifier",
        "model_parameters": parameters,
        "best_iteration": best_iteration,
        "load_time_seconds": round(load_time, 6),
        "training_time_seconds": round(training_time, 6),
        "auc_roc": round(float(roc_auc_score(y_test, fraud_probability)), 6),
        "accuracy": round(float(accuracy_score(y_test, prediction)), 6),
        "precision": round(float(precision_score(y_test, prediction, zero_division=0)), 6),
        "recall": round(float(recall_score(y_test, prediction, zero_division=0)), 6),
        "f1_score": round(float(f1_score(y_test, prediction, zero_division=0)), 6),
        "confusion_matrix": {
            "true_negative": int(tn),
            "false_positive": int(fp),
            "false_negative": int(fn),
            "true_positive": int(tp),
        },
        "inference_latency_ms_one_row": round(float(np.mean(latency_measurements_ms)), 6),
        "inference_latency_p95_ms_one_row": round(
            float(np.percentile(latency_measurements_ms, 95)), 6
        ),
        "inference_batch_size": int(len(batch)),
        "inference_throughput_rows_per_second": round(float(throughput), 3),
        "units": {
            "load_time": "seconds",
            "training_time": "seconds",
            "inference_latency": "milliseconds per row",
            "inference_throughput": "rows per second",
        },
    }

    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"\nSaved benchmark results to {args.output.resolve()}")


if __name__ == "__main__":
    main()
