import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Patient, Assessment, AuditLog
from .predictor import predict

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    assessments = Assessment.query.order_by(Assessment.created_at.desc()).limit(10).all()
    return render_template("dashboard.html", patients=patients, assessments=assessments)

@main_bp.route("/patient/new", methods=["GET","POST"])
@login_required
def new_patient():
    if request.method == "POST":
        code = "NG-" + str(Patient.query.count()+1).zfill(5)
        p = Patient(
            patient_code=code,
            name=request.form.get("name","").strip(),
            dob=request.form.get("dob"),
            gestational_age=float(request.form.get("gestational_age") or 0),
            birth_weight=float(request.form.get("birth_weight") or 0),
            sex=request.form.get("sex"),
            delivery_mode=request.form.get("delivery_mode"),
            apgar_1=int(request.form.get("apgar_1") or 0),
            apgar_5=int(request.form.get("apgar_5") or 0),
        )
        db.session.add(p)
        db.session.flush()
        db.session.add(AuditLog(user_id=current_user.id, patient_id=p.id, action="CREATE_PATIENT"))
        db.session.commit()
        return redirect(url_for("main.assessment", patient_id=p.id))
    return render_template("patient_new.html")

@main_bp.route("/patient/<int:patient_id>/assessment", methods=["GET","POST"])
@login_required
def assessment(patient_id):
    patient = db.session.get(Patient, patient_id)
    if not patient:
        return "Patient not found", 404
    result = None
    if request.method == "POST":
        payload = request.form.to_dict()
        payload["gestational_age"] = patient.gestational_age
        payload["birth_weight"] = patient.birth_weight
        result = predict(payload)
        a = Assessment(
            patient_id=patient.id,
            created_by=current_user.id,
            payload_json=json.dumps(payload),
            risk_probability=result["probability"],
            risk_category=result["category"],
            data_quality=result["quality"]
        )
        db.session.add(a)
        db.session.add(AuditLog(user_id=current_user.id, patient_id=patient.id, action="RUN_ASSESSMENT"))
        db.session.commit()
    history = Assessment.query.filter_by(patient_id=patient.id).order_by(Assessment.created_at.asc()).all()
    return render_template("assessment.html", patient=patient, result=result, history=history)

@main_bp.route("/patient/<int:patient_id>")
@login_required
def patient(patient_id):
    p = db.session.get(Patient, patient_id)
    if not p:
        return "Patient not found", 404
    return render_template("patient.html", patient=p)

@main_bp.route("/patient/<int:patient_id>/delete", methods=["POST"])
@login_required
def delete_patient(patient_id):
    p = db.session.get(Patient, patient_id)
    if p:
        db.session.add(AuditLog(user_id=current_user.id, patient_id=patient_id, action="DELETE_PATIENT"))
        db.session.delete(p)
        db.session.commit()
    return redirect(url_for("main.dashboard"))
