"""
RiskCheck model - stores the result of a symptom-based risk assessment.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class RiskCheck(Base):
    __tablename__ = "risk_checks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    disease = Column(String(100), nullable=False)
    risk_level = Column(String(20), nullable=False)      # Low | Medium | High
    confidence = Column(Integer, nullable=False)          # 0-100
    matched_symptoms = Column(String(500), nullable=False)  # comma-separated symptom names
    recommendation = Column(String(500), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="risk_checks")
