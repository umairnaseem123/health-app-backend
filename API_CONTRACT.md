# API Contract — AI Health Monitoring & Early Virus Risk Detection Platform

Base URL: `http://localhost:8000/api/v1`

All responses use this envelope:
```json
{
  "success": true,
  "message": "Human readable message",
  "data": { }
}
```

Authenticated endpoints require header:
```
Authorization: Bearer <access_token>
```

---

## 1. Auth — `/auth`

### POST `/auth/register`
Register a new user.
**Body:**
```json
{
  "full_name": "Ali Khan",
  "email": "ali@example.com",
  "password": "secret123",
  "phone_number": "+923001234567",
  "age": 29,
  "gender": "male",
  "emergency_contact_name": "Sara Khan",
  "emergency_contact_phone": "+923009876543"
}
```
**Response:** `201` → user object (no password)

### POST `/auth/login`
**Body:** `{ "email": "ali@example.com", "password": "secret123" }`
**Response:** `{ "access_token", "refresh_token", "token_type": "bearer" }`

### POST `/auth/refresh`
**Body:** `{ "refresh_token": "..." }` → new access + refresh tokens

### GET `/auth/me` 🔒
Returns the logged-in user's profile.

### PUT `/auth/me` 🔒
Update profile fields (all optional): full_name, phone_number, age, gender,
emergency_contact_name, emergency_contact_phone.

---

## 2. Blood Pressure & Vitals — `/bp` 🔒 (all endpoints require auth)

### POST `/bp`
Log a new vitals reading.
```json
{
  "systolic": 120,
  "diastolic": 80,
  "pulse_rate": 72,
  "spo2": 98.0,
  "temperature": 36.8,
  "notes": "Morning reading"
}
```

### GET `/bp?skip=0&limit=50`
Paginated list of the user's vitals history.

### GET `/bp/latest`
Most recent vitals reading.

### DELETE `/bp/{bp_log_id}`
Delete a specific vitals entry.

---

## 3. Symptoms & Risk Detection — `/symptoms` 🔒

### POST `/symptoms`
Log a symptom. Automatically re-runs the AI risk engine afterward.
```json
{ "symptom_name": "fever", "severity": 3, "duration_days": 2, "notes": "started last night" }
```

### GET `/symptoms?skip=0&limit=50`
Paginated symptom history.

### DELETE `/symptoms/{symptom_id}`

### POST `/symptoms/risk-check`
Manually recompute risk from the latest vitals + last 7 days of symptoms.
**Response data:**
```json
{
  "id": "...",
  "risk_score": 42.0,
  "risk_level": "moderate",
  "contributing_factors": ["high_blood_pressure", "symptom:fever"],
  "recommendation": "Some risk indicators found. Rest, stay hydrated...",
  "created_at": "..."
}
```

### GET `/symptoms/risk-check/latest`
Fetch the most recent risk check result.

---

## 4. Reports — `/reports` 🔒

### POST `/reports/generate`
```json
{ "period_start": "2026-06-01T00:00:00", "period_end": "2026-06-30T23:59:59", "title": "June Health Report" }
```
Aggregates BP logs, symptoms, and risk checks in that period into a saved report.

### GET `/reports?skip=0&limit=20`
List generated reports.

### GET `/reports/{report_id}`
Full report detail including `data_snapshot`.

### DELETE `/reports/{report_id}`

---

## 5. Dashboard — `/dashboard` 🔒

### GET `/dashboard`
Home-screen summary: latest vitals, latest risk status, active symptom count
(last 7 days), 14-point BP trend, and lifetime totals.

---

## 6. Emergency — `/emergency` 🔒

### PUT `/emergency/contact`
```json
{ "emergency_contact_name": "Sara Khan", "emergency_contact_phone": "+923009876543" }
```

### GET `/emergency/contact`

### POST `/emergency/alert`
```json
{ "reason": "Severe chest pain and high risk score", "current_location": "DHA Phase 5, Karachi" }
```
Dispatches an alert to the user's configured emergency contact (SMS/email
provider integration is stubbed — plug in Twilio/SendGrid/etc. in
`app/api/v1/emergency.py`).

---

## Risk Score Model (rule-based, explainable)

Computed in `app/core/risk_engine.py` from the latest vitals + symptoms
logged in the last 7 days:

| Factor | Points |
|---|---|
| Systolic ≥140 or Diastolic ≥90 | +25 |
| Systolic ≤90 or Diastolic ≤60 | +15 |
| Pulse <50 or >100 bpm | +15 |
| SpO2 < 94% | +25 |
| Temperature ≥ 38.0°C | +20 |
| Each symptom | +7 to +15 (by severity) |
| High-severity symptom (fever, chest pain, breathing difficulty) | +10 extra |

Score is capped at 100 and mapped to: `low` (<25), `moderate` (<50),
`high` (<75), `critical` (≥75).
