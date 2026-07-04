"""
Blood pressure logging endpoints - paths and response shapes follow
API_CONTRACT.md exactly.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api.deps import get_current_user, get_db
from app.core.response import success_response
from app.models.bp_log import BPLog
from app.models.user import User
from app.schemas.bp import BPLogCreate

router = APIRouter(prefix="/bp", tags=["Blood Pressure"])


def compute_status(systolic: int, diastolic: int):
    """
    Keep these thresholds and exact label strings in sync with the frontend's
    STATUS_COLORS maps in BPTrackerPage.jsx / HistoryPage.jsx.
    """
    if systolic >= 180 or diastolic >= 120:
        return "Hypertensive Crisis", "Seek emergency care immediately."
    if systolic >= 140 or diastolic >= 90:
        return "High", "Reduce salt intake, avoid caffeine, consult a doctor within a week."
    if 120 <= systolic < 140:
        return "Elevated", "Monitor regularly, reduce sodium, stay active."
    if systolic < 90 or diastolic < 60:
        return "Low", "Stay hydrated, avoid sudden posture changes, consult if dizzy."
    return "Normal", "Great job! Keep maintaining a healthy lifestyle."


@router.post("/log/")
def log_bp(
    payload: BPLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    status_label, advice = compute_status(payload.systolic, payload.diastolic)
    entry = BPLog(
        user_id=current_user.id,
        systolic=payload.systolic,
        diastolic=payload.diastolic,
        status=status_label,
        advice=advice,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return success_response(
        "Vitals logged successfully",
        {
            "id": entry.id,
            "systolic": entry.systolic,
            "diastolic": entry.diastolic,
            "status": entry.status,
            "advice": entry.advice,
            "created_at": entry.created_at,
        },
    )


@router.get("/history/")
def get_history(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entries = (
        db.query(BPLog)
        .filter(BPLog.user_id == current_user.id)
        .order_by(desc(BPLog.created_at))
        .limit(days)
        .all()
    )
    data = [
        {
            "date": e.created_at.strftime("%b %d"),
            "systolic": e.systolic,
            "diastolic": e.diastolic,
            "status": e.status,
        }
        for e in reversed(entries)
    ]
    return success_response("Vitals fetched", data)


@router.get("/latest/")
def get_latest(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (
        db.query(BPLog)
        .filter(BPLog.user_id == current_user.id)
        .order_by(desc(BPLog.created_at))
        .first()
    )
    if entry is None:
        return success_response("No BP readings logged yet", None)

    return success_response(
        "Latest vitals fetched",
        {
            "systolic": entry.systolic,
            "diastolic": entry.diastolic,
            "status": entry.status,
            "advice": entry.advice,
        },
    )
