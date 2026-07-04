# AI Health Monitoring & Early Virus Risk Detection Platform — Backend

FastAPI + SQLAlchemy backend with JWT auth, blood-pressure/vitals logging,
symptom tracking, a rule-based AI risk-scoring engine, health report
generation, a dashboard summary endpoint, and emergency alert triggering.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and set a strong SECRET_KEY

uvicorn app.main:app --reload
```

App runs at: http://localhost:8000
Interactive docs (Swagger UI): http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

By default it uses SQLite (`health_platform.db`, auto-created on first run).
To use PostgreSQL instead, set `DATABASE_URL` in `.env` to a
`postgresql://user:password@host:port/dbname` string and
`pip install psycopg2-binary` (already in requirements.txt).

## Project Structure

```
backend/
├── requirements.txt
├── .env.example
├── API_CONTRACT.md          <- full endpoint documentation
└── app/
    ├── main.py               <- FastAPI app, routers, CORS, error handlers
    ├── core/
    │   ├── config.py         <- settings from .env
    │   ├── database.py       <- SQLAlchemy engine/session
    │   ├── security.py       <- password hashing + JWT
    │   ├── response.py       <- standard {success, message, data} envelope
    │   └── risk_engine.py    <- rule-based AI risk scoring logic
    ├── models/                <- SQLAlchemy ORM models
    ├── schemas/                <- Pydantic request/response schemas
    └── api/
        ├── deps.py            <- get_current_user auth dependency
        └── v1/                <- route handlers per feature
```

## Auth flow

1. `POST /api/v1/auth/register`
2. `POST /api/v1/auth/login` → get `access_token` + `refresh_token`
3. Send `Authorization: Bearer <access_token>` on all protected routes
4. `POST /api/v1/auth/refresh` with `refresh_token` when access token expires

## Notes

- The risk-scoring model in `app/core/risk_engine.py` is a transparent,
  rule-based heuristic — not a medical diagnostic tool. It's meant to flag
  patterns worth attention and always recommends professional consultation
  when risk is elevated.
- Emergency SMS/email sending in `app/api/v1/emergency.py` is stubbed with a
  `print()` — wire in a real provider (Twilio, SendGrid, Firebase, etc.)
  using the `SMS_PROVIDER_API_KEY` / `EMAIL_PROVIDER_API_KEY` settings.
- For production, replace `init_db()` (create_all) with Alembic migrations.
