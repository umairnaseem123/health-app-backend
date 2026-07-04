"""
Symptom checker & risk-check endpoints - paths and response shapes follow
API_CONTRACT.md exactly.
"""
from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_db
from app.core.response import success_response
from app.models.risk_check import RiskCheck
from app.models.symptom import Symptom
from app.models.user import User
from app.schemas.symptoms import RiskCheckRequest

router = APIRouter(tags=["Symptom Checker"])


@router.get("/symptoms/")
def list_symptoms(db: Session = Depends(get_db)):
    symptoms = db.query(Symptom).order_by(Symptom.id).all()
    data = [{"id": s.id, "name": s.name, "category": s.category} for s in symptoms]
    return success_response("Symptoms fetched", data)


@router.post("/risk-check/")
def check_risk(
    payload: RiskCheckRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Simple rule-based check matching app/api/v1/../../../frontend mock logic
    (fever + cough => Flu). Swap this body for a real model later - keep the
    request/response shape identical.
    """
    matched = db.query(Symptom).filter(Symptom.id.in_(payload.symptom_ids)).all()
    matched_names = [s.name for s in matched]

    has_fever = 1 in payload.symptom_ids
    has_cough = 3 in payload.symptom_ids
    disease = "Flu" if (has_fever and has_cough) else "Common Cold"
    risk_level = "Medium" if len(payload.symptom_ids) >= 5 else "Low"
    confidence = 87 if (has_fever and has_cough) else 62
    recommendation = (
        "Monitor for 48 hours. Consult a doctor if symptoms worsen."
        if risk_level == "Medium"
        else "Rest and stay hydrated. Symptoms should improve in a few days."
    )

    entry = RiskCheck(
        user_id=current_user.id,
        disease=disease,
        risk_level=risk_level,
        confidence=confidence,
        matched_symptoms=",".join(matched_names),
        recommendation=recommendation,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return success_response(
        "Risk check completed",
        {
            "prediction_id": entry.id,
            "disease": disease,
            "risk_level": risk_level,
            "confidence": confidence,
            "matched_symptoms": matched_names,
            "recommendation": recommendation,
        },
    )


@router.get("/risk-check/history/")
def risk_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entries = (
        db.query(RiskCheck)
        .filter(RiskCheck.user_id == current_user.id)
        .order_by(desc(RiskCheck.created_at))
        .all()
    )
    data = [
        {
            "id": e.id,
            "date": e.created_at.strftime("%Y-%m-%d"),
            "disease": e.disease,
            "risk_level": e.risk_level,
            "confidence": e.confidence,
        }
        for e in entries
    ]
    return success_response("Risk check history fetched", data)
