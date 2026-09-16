import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

MODEL_DIR = Path(__file__).resolve().parents[1] / "ml" / "artifacts"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "neoguard_model.joblib"

FEATURES = [
    "gestational_age","birth_weight","maternal_fever","prom_gt_18h",
    "chorioamnionitis","gbs_positive","iugr_sga","temperature",
    "heart_rate","spo2","respiratory_rate","capillary_refill",
    "crp","pct","lactate","wbc","platelets","it_ratio","ph","base_excess"
]

def load_model():
    if not MODEL_PATH.exists():
        from ml.train_demo import train
        train()
    return joblib.load(MODEL_PATH)

def _to_num(value, default=np.nan):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def prepare(payload):
    row = {}
    for f in FEATURES:
        row[f] = _to_num(payload.get(f))
    return pd.DataFrame([row], columns=FEATURES)

def predict(payload):
    model = load_model()
    df = prepare(payload)
    probability = float(model.predict_proba(df)[0, 1]) * 100
    missing = [c for c in FEATURES if pd.isna(df.iloc[0][c])]
    quality = "Good" if len(missing) <= 2 else ("Limited" if len(missing) <= 6 else "Poor")
    if probability >= 70:
        category = "Elevated"
    elif probability >= 35:
        category = "Intermediate"
    else:
        category = "Lower"
    contributions = explain(payload, model)
    return {
        "probability": round(probability, 1),
        "category": category,
        "quality": quality,
        "missing": missing,
        "contributions": contributions,
        "model_version": "NeoGuard-demo-v1"
    }

def explain(payload, model):
    # Transparent, model-agnostic clinical feature contribution display.
    # For the demo model we estimate local contribution by perturbing one feature.
    base = prepare(payload)
    base_prob = float(model.predict_proba(base)[0,1])
    results = []
    for feature in FEATURES:
        if pd.isna(base.iloc[0][feature]):
            continue
        altered = base.copy()
        val = float(altered.iloc[0][feature])
        altered.iloc[0, altered.columns.get_loc(feature)] = val * 0.90 if val else 0.1
        new_prob = float(model.predict_proba(altered)[0,1])
        delta = base_prob - new_prob
        results.append((feature, delta))
    results.sort(key=lambda x: abs(x[1]), reverse=True)
    labels = {
        "gestational_age":"Gestational age","birth_weight":"Birth weight",
        "maternal_fever":"Maternal fever","prom_gt_18h":"PROM >18h",
        "chorioamnionitis":"Chorioamnionitis","gbs_positive":"GBS positive",
        "iugr_sga":"IUGR / SGA","temperature":"Temperature",
        "heart_rate":"Heart rate","spo2":"SpO₂","respiratory_rate":"Respiratory rate",
        "capillary_refill":"Capillary refill","crp":"CRP","pct":"Procalcitonin",
        "lactate":"Lactate","wbc":"WBC","platelets":"Platelets",
        "it_ratio":"I:T ratio","ph":"pH","base_excess":"Base excess"
    }
    return [{"feature": labels.get(k,k), "direction": "raises" if d > 0 else "lowers", "strength": round(abs(d)*100, 1)} for k,d in results[:6]]
