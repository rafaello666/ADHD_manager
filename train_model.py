# train_model.py

"""
Moduł trenujący model uczenia maszynowego na podstawie historii zadań.
"""

import os
import json
import numpy as np
from typing import List, Tuple

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

HISTORY_FILE = "task_history.json"
MODEL_FILE = "model_priority.pkl"

def load_history():
    """
    Wczytuje historię zadań z pliku JSON.

    Zwraca:
        Lista rekordów historii.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Wczytywanie {HISTORY_FILE}: {e}")
        return []

def extract_features_and_target(records) -> Tuple[np.ndarray, np.ndarray]:
    """
    Ekstrahuje cechy i zmienne docelowe do trenowania modelu.

    Args:
        records: Lista rekordów historii.

    Zwraca:
        Krotka (X, y) z cechami i zmiennymi docelowymi.
    """
    X_list = []
    y_list = []
    for r in records:
        if r.get("user_importance") is None:
            continue
        sp = float(r.get("system_priority", 0.0))
        ts = float(r.get("time_spent", 0.0))
        dg = float(r.get("actual_deadline_gap", 0.0))
        wi = 1.0 if r.get("was_interrupted") else 0.0
        feats = [sp, ts, dg, wi]
        X_list.append(feats)
        y_list.append(float(r["user_importance"]))

    X = np.array(X_list, dtype=float)
    y = np.array(y_list, dtype=float)
    return X, y

def main():
    recs = load_history()
    X, y = extract_features_and_target(recs)
    if len(X) < 5:
        print("Za mało danych do trenowania (<5).")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"[TRAIN] Mean Absolute Error: {mae:.3f}")

    joblib.dump(model, MODEL_FILE)
    print(f"[TRAIN] Zapisano model do {MODEL_FILE}")

if __name__ == "__main__":
    main()