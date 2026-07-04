"""
Pydantic schemas for the symptom checker & risk-check endpoints.
"""
from typing import List

from pydantic import BaseModel


class SymptomOut(BaseModel):
    id: int
    name: str
    category: str


class RiskCheckRequest(BaseModel):
    symptom_ids: List[int]


class RiskCheckResponse(BaseModel):
    prediction_id: str
    disease: str
    risk_level: str
    confidence: int
    matched_symptoms: List[str]
    recommendation: str


class RiskHistoryItem(BaseModel):
    id: str
    date: str
    disease: str
    risk_level: str
    confidence: int
