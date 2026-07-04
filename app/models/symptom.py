"""
Symptom model - a FIXED CATALOG of selectable symptoms (not a per-user log).

The frontend's symptom checker page calls GET /symptoms/ to render a grid of
checkboxes, then submits the chosen ids to POST /risk-check/. This table is
seeded once on startup (see app/core/database.py: seed_symptoms) and never
changes at runtime.
"""
from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False)  # General | Respiratory | Digestive | Cardiac | Other
