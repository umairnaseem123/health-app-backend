"""
Pydantic schemas for the dashboard endpoints.
"""
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_scans: int
    latest_risk_level: str
    latest_bp_status: str
    reports_count: int


class BPTrendItem(BaseModel):
    date: str
    systolic: int
    diastolic: int
