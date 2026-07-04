"""
BPLog model - stores a single blood-pressure reading for a user, along with
the computed status label and advice text the frontend displays directly.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class BPLog(Base):
    __tablename__ = "bp_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    systolic = Column(Integer, nullable=False)
    diastolic = Column(Integer, nullable=False)

    # Computed once at creation time by app/core/bp_rules.py — the frontend
    # reads these two fields directly, so they must always be one of the
    # exact strings defined in bp_rules.compute_status().
    status = Column(String(30), nullable=False)
    advice = Column(String(300), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="bp_logs")
