import argparse
import json
import os
import platform
import time

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, early_stopping, log_evaluation
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split


def load_data(csv_path, synthetic_rows, random_state):
    started = time.perf_counter()
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if "Class" not in df.columns:
            raise ValueError(f"{csv_path} must contain a Class target column")
        y = df["Class"].astype(int)
        x = df.drop(columns=["Class"])
        source = f"csv:{csv_path}"
    else:
        x, y = make_classification(
            n_samples=synthetic_rows,
            n_features=30,
            n_informative=12,
            n_redundant=8,
            n_repeated=0,
            n_clusters_per_class=3,
            weights=[0.998, 0.002],
            class_sep=2.0,
            flip_y=0.001,
            random_state=random_state,
        )
        x = pd.DataFrame(x, columns=[f"V{i}" for i in range(1, 31)])
        y = pd.Series(y, name="Class")
        source = "synthetic_credit_card_like"

    load_seconds = time.perf_counter() - started
    return x, y, source, load_seconds


def main():
    parser = argparse.ArgumentParser(description="LightGBM CPU benchmark for Day16 fallback lab.")
    parser.add_argument("--csv", default="creditcard.csv", help="Path to Kaggle creditcard.csv if available.")
    parser.add_argument("--synthetic-rows", type=int, default=284807)
    parser.add_argument("--output", default="benchmark_result.json")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    total_started = time.perf_counter()
    x, y, source, load_seconds = load_data(args.csv, args.synthetic_rows, args.random_state)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=args.random_state,
        stratify=y,
    )

    model = LGBMClassifier(
        objective="binary",
        n_estimators=600,
        learning_rate=0.05,
        num_leaves=64,
        subsample=0.85,
        colsample_bytree=0.85,
        class_weight="balanced",
        n_jobs=-1,
        random_state=args.random_state,
    )

    training_started = time.perf_counter()
    model.fit(
        x_train,
        y_train,
        eval_set=[(x_test, y_test)],
        eval_metric="auc",
        callbacks=[early_stopping(30), log_evaluation(50)],
    )
    training_seconds = time.perf_counter() - training_started

    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    one_row = x_test.iloc[[0]]
    latency_started = time.perf_counter()
    model.predict_proba(one_row)
    latency_ms = (time.perf_counter() - latency_started) * 1000

    batch = x_test.iloc[:1000]
    throughput_started = time.perf_counter()
    model.predict_proba(batch)
    throughput_seconds = time.perf_counter() - throughput_started
    throughput_rows_per_second = len(batch) / throughput_seconds

    result = {
        "dataset_source": source,
        "rows": int(len(x)),
        "features": int(x.shape[1]),
        "positive_rate": float(np.mean(y)),
        "load_data_seconds": round(load_seconds, 4),
        "training_seconds": round(training_seconds, 4),
        "best_iteration": int(getattr(model, "best_iteration_", 0) or model.n_estimators),
        "auc_roc": round(float(roc_auc_score(y_test, probabilities)), 6),
        "accuracy": round(float(accuracy_score(y_test, predictions)), 6),
        "f1_score": round(float(f1_score(y_test, predictions, zero_division=0)), 6),
        "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 6),
        "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 6),
        "inference_latency_1_row_ms": round(latency_ms, 4),
        "inference_throughput_1000_rows_per_second": round(throughput_rows_per_second, 2),
        "total_seconds": round(time.perf_counter() - total_started, 4),
        "python": platform.python_version(),
        "machine": platform.machine(),
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("Day16 CPU LightGBM benchmark complete")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
