from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(40), default="clinician")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="scrypt")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_code = db.Column(db.String(40), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.String(30))
    gestational_age = db.Column(db.Float)
    birth_weight = db.Column(db.Float)
    sex = db.Column(db.String(20))
    delivery_mode = db.Column(db.String(30))
    apgar_1 = db.Column(db.Integer)
    apgar_5 = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assessments = db.relationship("Assessment", backref="patient", lazy=True, cascade="all, delete-orphan")

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    payload_json = db.Column(db.Text, nullable=False)
    risk_probability = db.Column(db.Float)
    risk_category = db.Column(db.String(40))
    data_quality = db.Column(db.String(40))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    action = db.Column(db.String(160), nullable=False)
    patient_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
