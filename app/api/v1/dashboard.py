"""
Dashboard summary endpoints - paths and response shapes follow
API_CONTRACT.md exactly.
"""
from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_db
from app.core.response import success_response
from app.models.bp_log import BPLog
from app.models.report import Report
from app.models.risk_check import RiskCheck
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary/")
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_scans = db.query(RiskCheck).filter(RiskCheck.user_id == current_user.id).count()
    reports_count = db.query(Report).filter(Report.user_id == current_user.id).count()

    latest_risk = (
        db.query(RiskCheck)
        .filter(RiskCheck.user_id == current_user.id)
        .order_by(desc(RiskCheck.created_at))
        .first()
    )
    latest_bp = (
        db.query(BPLog)
        .filter(BPLog.user_id == current_user.id)
        .order_by(desc(BPLog.created_at))
        .first()
    )

    data = {
        "total_scans": total_scans,
        "latest_risk_level": latest_risk.risk_level if latest_risk else "N/A",
        "latest_bp_status": latest_bp.status if latest_bp else "N/A",
        "reports_count": reports_count,
    }
    return success_response("Dashboard summary fetched", data)


@router.get("/bp-trend/")
def bp_trend(
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
        {"date": e.created_at.strftime("%b %d"), "systolic": e.systolic, "diastolic": e.diastolic}
        for e in reversed(entries)
    ]
    return success_response("BP trend fetched", data)
