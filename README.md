# NeoGuard AI — Complete End-to-End Prototype

NeoGuard is a secure, explainable neonatal sepsis **risk-screening / clinical decision-support research prototype**.

It includes:

- Modern responsive hospital-style UI
- Landing page
- Secure login/register
- Password hashing with scrypt
- CSRF protection
- Session hardening
- Role field ready for RBAC
- Patient management
- Five-step clinical assessment flow
- Risk probability model
- Calibrated Random Forest demonstration model
- Missing-data / data-quality status
- Local model contribution explanation
- Assessment history
- Audit logging
- SQLite database for local development
- Production-oriented project structure

## Important clinical limitation

This repository is a **research/education prototype**. The included model is trained on synthetic demonstration data so the application can run immediately. Its displayed probability is NOT clinically validated and must not be used to diagnose or treat a patient.

For real research, replace the demonstration training set with an appropriately governed neonatal dataset and perform patient-level/time-aware validation, calibration, subgroup analysis, external validation and prospective clinical validation.

## Evidence base used for project design

The workflow is informed by:

1. WHO recommendations for serious bacterial infections in infants aged 0–59 days.
2. Published neonatal sepsis machine-learning work using EHR data from NICU episodes.
3. Neonatal sepsis metadata standards for structured research data collection.

The project deliberately does not automatically prescribe antibiotics.

## Run on Windows

Open PowerShell in this folder:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m ml.train_demo
python run.py
```

Open:

http://127.0.0.1:5000

Demo login:

- Email: `demo@neoguard.local`
- Password: `NeoGuard@2026`

## Production checklist

Before any real patient use:

- Use HTTPS
- Use PostgreSQL instead of SQLite
- Put secrets in a secret manager
- Add MFA / hospital SSO
- Implement strict role-based and organization-level access control
- Encrypt data at rest and in transit
- Minimize patient identifiers
- Add consent and retention controls
- Add complete audit logging
- Validate the model on independent clinical data
- Calibrate the model
- Evaluate sensitivity, specificity, PPV, NPV, AUROC, AUPRC and Brier score
- Perform subgroup/fairness analysis
- Perform prospective validation
- Complete institutional ethics / governance review
- Conduct applicable medical-device / SaMD regulatory assessment
- Have a neonatologist and clinical governance team approve clinical content

## Data

`data/README.md` explains the recommended public evidence/data sources and how to replace the synthetic demonstration data.
