"""
Report upload endpoints - paths and response shapes follow API_CONTRACT.md
exactly. The frontend uploads a file, then polls GET /reports/{id}/ every
couple seconds until status is "completed" or "failed".
"""
import json
import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.response import success_response
from app.models.report import Report
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Reports"])

UPLOAD_DIR = "uploads/reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload/")
def upload_report(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    TODO: replace the body below with a real async OCR job (e.g. Celery task
    running Tesseract) that fills in extracted_json / analysis_json and flips
    status to "completed". For now the file is saved and left "processing".
    """
    ext = os.path.splitext(file.filename or "")[1]
    saved_name = f"{uuid.uuid4().hex}{ext}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)

    with open(saved_path, "wb") as f:
        f.write(file.file.read())

    report = Report(user_id=current_user.id, file_path=saved_path, status="processing")
    db.add(report)
    db.commit()
    db.refresh(report)

    return success_response("Report uploaded, processing started", {"report_id": report.id, "status": report.status})


@router.get("/{report_id}/")
def get_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = (
        db.query(Report)
        .filter(Report.id == report_id, Report.user_id == current_user.id)
        .first()
    )
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    data = {"report_id": report.id, "status": report.status}
    if report.extracted_json:
        data["extracted"] = json.loads(report.extracted_json)
    if report.analysis_json:
        data["analysis"] = json.loads(report.analysis_json)

    return success_response("Report status fetched", data)
