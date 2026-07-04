"""
Pydantic schemas for blood pressure endpoints.
"""
from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class BPLogCreate(BaseModel):
    systolic: int = Field(..., ge=50, le=300)
    diastolic: int = Field(..., ge=30, le=200)

    @model_validator(mode="after")
    def check_systolic_greater_than_diastolic(self):
        if self.diastolic >= self.systolic:
            raise ValueError("diastolic must be lower than systolic")
        return self


class BPLogResponse(BaseModel):
    id: str
    systolic: int
    diastolic: int
    status: str
    advice: str
    created_at: datetime


class BPHistoryItem(BaseModel):
    date: str
    systolic: int
    diastolic: int
    status: str


class BPLatestResponse(BaseModel):
    systolic: int
    diastolic: int
    status: str
    advice: str
