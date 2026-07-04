"""
Pydantic schemas for report upload & retrieval endpoints.
"""
from typing import Optional

from pydantic import BaseModel


class ReportUploadResponse(BaseModel):
    report_id: str
    status: str  # "processing"


class ReportExtracted(BaseModel):
    wbc: Optional[int] = None
    platelets: Optional[int] = None
    sugar: Optional[int] = None


class ReportAnalysis(BaseModel):
    wbc_flag: Optional[str] = None
    sugar_flag: Optional[str] = None


class ReportStatusResponse(BaseModel):
    report_id: str
    status: str  # processing | completed | failed
    extracted: Optional[ReportExtracted] = None
    analysis: Optional[ReportAnalysis] = None
