"""
Report model - an uploaded blood test report file, processed asynchronously
(OCR/extraction) and polled by the frontend until status is "completed".
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    file_path = Column(String(500), nullable=False)
    status = Column(String(20), nullable=False, default="processing")  # processing | completed | failed

    extracted_json = Column(Text, nullable=True)   # JSON string: {"wbc":.., "platelets":.., "sugar":..}
    analysis_json = Column(Text, nullable=True)     # JSON string: {"wbc_flag":.., "sugar_flag":..}

    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="reports")
