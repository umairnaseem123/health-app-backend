"""
Database engine, session factory and declarative Base.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

connect_args = {}
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    # Needed only for SQLite when used with multiple threads (FastAPI dev server)
    connect_args = {"check_same_thread": False}
elif "pg8000" in settings.DATABASE_URL:
    # pg8000 doesn't understand the "sslmode" query param psycopg2 uses -
    # it needs an explicit ssl_context instead. True makes it use a default
    # SSL context, which is what Neon (and most managed Postgres) requires.
    connect_args = {"ssl_context": True}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


DEFAULT_SYMPTOMS = [
    ("Fever", "General"), ("Headache", "General"), ("Cough", "Respiratory"),
    ("Fatigue", "General"), ("Nausea", "Digestive"), ("Sore Throat", "Respiratory"),
    ("Shortness of Breath", "Respiratory"), ("Body Pain", "General"),
    ("Loss of Taste", "Other"), ("Loss of Smell", "Other"), ("Chest Pain", "Cardiac"),
    ("Chills", "General"), ("Diarrhea", "Digestive"), ("Joint Pain", "General"),
    ("Skin Rash", "Other"), ("Runny Nose", "Respiratory"), ("Dizziness", "Other"),
    ("Vomiting", "Digestive"), ("Eye Pain", "Other"), ("Abdominal Pain", "Digestive"),
]


def init_db() -> None:
    """
    Create all tables and seed the symptom catalog. In production prefer
    Alembic migrations instead of create_all.
    """
    # Import models here so they are registered on Base.metadata before create_all
    from app.models import user, bp_log, symptom, risk_check, report  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _seed_symptoms()


def _seed_symptoms() -> None:
    """
    Seeds the symptoms table exactly once, in the exact order defined in
    API_CONTRACT.md, so ids 1-20 stay fixed (id 1 = Fever, id 3 = Cough are
    hardcoded in app/api/v1/symptoms.py's risk-check rule logic).
    """
    from app.models.symptom import Symptom

    db = SessionLocal()
    try:
        if db.query(Symptom).count() == 0:
            for name, category in DEFAULT_SYMPTOMS:
                db.add(Symptom(name=name, category=category))
            db.commit()
    finally:
        db.close()


def get_db():
    """
    FastAPI dependency that yields a DB session and ensures it's closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
