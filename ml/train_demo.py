from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "ml" / "artifacts"
ARTIFACT.mkdir(parents=True, exist_ok=True)
FEATURES = [
    "gestational_age","birth_weight","maternal_fever","prom_gt_18h",
    "chorioamnionitis","gbs_positive","iugr_sga","temperature",
    "heart_rate","spo2","respiratory_rate","capillary_refill",
    "crp","pct","lactate","wbc","platelets","it_ratio","ph","base_excess"
]

def make_demo_data(n=3500, seed=42):
    rng = np.random.default_rng(seed)
    ga = rng.normal(34, 4, n).clip(24, 41)
    bw = (ga - 24) * 0.12 + rng.normal(.35, .18, n)
    fever = rng.binomial(1, .12, n)
    prom = rng.binomial(1, .20, n)
    chorio = rng.binomial(1, .06, n)
    gbs = rng.binomial(1, .10, n)
    iugr = rng.binomial(1, .14, n)
    temp = rng.normal(36.7, .45, n)
    hr = rng.normal(145, 25, n)
    spo2 = rng.normal(95, 3.5, n).clip(75,100)
    rr = rng.normal(48, 12, n)
    cap = rng.normal(2.0, .7, n).clip(.5,5)
    crp = np.maximum(0, rng.lognormal(0.1, .8, n) + fever*3 + chorio*4)
    pct = np.maximum(0, rng.lognormal(-.3, .7, n) + chorio*1.5)
    lactate = np.maximum(.5, rng.normal(2.2, .9, n) + (100-spo2)*.04)
    wbc = rng.normal(12, 5, n).clip(1,35)
    platelets = rng.normal(220, 75, n).clip(30,450)
    it = rng.beta(2,12,n).clip(0,.8)
    ph = rng.normal(7.35,.09,n).clip(6.9,7.55)
    be = rng.normal(0,4,n)
    linear = (
        -2.5 + (34-ga)*.16 + (bw<1.5)*.7 + fever*.7 + prom*.5 +
        chorio*1.1 + gbs*.35 + iugr*.4 + np.abs(temp-36.7)*1.1 +
        np.maximum(hr-170,0)*.018 + np.maximum(92-spo2,0)*.12 +
        np.maximum(rr-60,0)*.035 + np.maximum(cap-3,0)*.45 +
        np.maximum(crp-5,0)*.08 + np.maximum(pct-2,0)*.25 +
        np.maximum(lactate-3,0)*.25 + np.maximum(.2-it,0)*.4 +
        np.maximum(7.2-ph,0)*2 + np.maximum(-be,0)*.06
    )
    p = 1/(1+np.exp(-linear))
    y = rng.binomial(1,p)
    X = pd.DataFrame({
        "gestational_age":ga,"birth_weight":bw,"maternal_fever":fever,
        "prom_gt_18h":prom,"chorioamnionitis":chorio,"gbs_positive":gbs,
        "iugr_sga":iugr,"temperature":temp,"heart_rate":hr,"spo2":spo2,
        "respiratory_rate":rr,"capillary_refill":cap,"crp":crp,"pct":pct,
        "lactate":lactate,"wbc":wbc,"platelets":platelets,"it_ratio":it,
        "ph":ph,"base_excess":be
    })
    return X, pd.Series(y, name="sepsis")

def train():
    X, y = make_demo_data()
    Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=.2,stratify=y,random_state=42)
    numeric = FEATURES
    pre = ColumnTransformer([("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ]), numeric)])
    rf = RandomForestClassifier(
        n_estimators=350, max_depth=7, min_samples_leaf=8,
        class_weight="balanced", random_state=42, n_jobs=-1
    )
    pipe = Pipeline([("pre",pre),("model",rf)])
    calibrated = CalibratedClassifierCV(pipe, method="sigmoid", cv=5)
    calibrated.fit(Xtr,ytr)
    pred = calibrated.predict_proba(Xte)[:,1]
    metrics = {
        "roc_auc_demo": float(roc_auc_score(yte,pred)),
        "average_precision_demo": float(average_precision_score(yte,pred)),
        "brier_demo": float(brier_score_loss(yte,pred)),
        "n_samples": int(len(X)),
        "note": "Synthetic demonstration data only; these metrics are not clinical validation."
    }
    joblib.dump(calibrated, ARTIFACT/"neoguard_model.joblib")
    (ARTIFACT/"metrics.json").write_text(pd.Series(metrics).to_json(indent=2))
    return metrics

if __name__ == "__main__":
    print(train())
