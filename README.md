# NeoGuard AI

## AI-Assisted Neonatal Sepsis Risk Estimation System

NeoGuard AI is an end-to-end healthcare research and educational prototype designed to estimate neonatal sepsis risk from clinical parameters using machine learning.

The system combines a secure web application, patient management, clinical assessment workflow, machine learning prediction, and explainable AI into a unified platform.

> **Disclaimer:** NeoGuard AI is a research and educational prototype. It is not a medical diagnostic device and must not be used to make clinical decisions.

---

## Project Overview

Neonatal sepsis is a serious condition where early recognition can be important. NeoGuard explores how machine learning can be used to provide an AI-assisted risk estimate from selected neonatal clinical parameters.

The application is designed around a simple workflow:

Patient Details  
↓  
Clinical Assessment  
↓  
Data Processing  
↓  
Machine Learning Model  
↓  
Sepsis Risk Estimate  
↓  
Explainable AI  
↓  
Assessment History

---

## Key Features

- Secure user authentication
- Patient registration and management
- Neonatal clinical assessment workflow
- Vital-sign and laboratory input
- AI-assisted sepsis risk estimation
- Explainable prediction factors
- Assessment history
- Audit logging
- Responsive healthcare-focused UI
- SQLite database for development
- Flask backend
- Machine learning pipeline

---

## Technology Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF

### Machine Learning
- Scikit-learn
- NumPy
- Pandas
- SHAP
- Joblib

### Database
- SQLite
- SQLAlchemy

### Frontend
- HTML5
- CSS3
- JavaScript

---

## Machine Learning

The current version contains a synthetic demonstration model intended for software development and demonstration purposes.

Current prototype metrics:

| Metric | Value |
|---|---:|
| ROC-AUC | 0.734 |
| Average Precision | 0.549 |
| Brier Score | 0.179 |
| Samples | 3,500 |

These metrics were obtained using synthetic demonstration data.

They do **not** represent clinical validation or real-world diagnostic accuracy.

The model will be upgraded in future work using appropriate neonatal clinical datasets and rigorous validation procedures.

---

## Explainable AI

NeoGuard is designed to provide interpretable information alongside the model's risk estimate.

Potential contributing clinical factors can be presented to help users understand which inputs influenced the model's prediction.

SHAP is included in the machine learning architecture for explainability research.

---

## Security

The prototype includes:

- Password hashing
- Authentication
- Session management
- CSRF protection
- Secure session configuration
- Audit logging
- Separation of sensitive configuration
- Protection against accidental upload of local databases and environment files

For real clinical deployment, additional security, privacy, regulatory, infrastructure, and clinical governance requirements would be necessary.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/niharika070706/NeoGuard-AI.git
cd NeoGuard-AI
