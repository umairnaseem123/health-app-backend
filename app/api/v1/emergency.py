"""
Emergency endpoints.

GET /emergency/nearby-doctors/ is the one the frontend's Emergency page
actually calls (see API_CONTRACT.md) - its response shape must not change.

The contact-management and SOS alert endpoints below are extra, optional
features kept from the original design; the frontend does not call them yet.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.response import success_response
from app.models.user import User
from app.schemas.emergency import DoctorOut  # noqa: F401 (response documents this shape)

router = APIRouter(prefix="/emergency", tags=["Emergency"])

# TODO: replace with a real `doctors` table filtered/sorted by (lat, lng),
# or a maps/places API call. Keep the response shape identical to DoctorOut.
_STATIC_DOCTORS = [
    {
        "id": 1,
        "name": "Dr. Ayesha Raza",
        "specialty": "General Physician",
        "hospital": "South City Hospital",
        "address": "Clifton Block 5, Karachi",
        "phone": "+92 21 3587 4444",
        "distance_km": 1.8,
    },
    {
        "id": 2,
        "name": "Dr. Bilal Sheikh",
        "specialty": "Internal Medicine",
        "hospital": "Aga Khan University Hospital",
        "address": "Stadium Road, Karachi",
        "phone": "+92 21 3486 1234",
        "distance_km": 3.2,
    },
]


@router.get("/nearby-doctors/")
def nearby_doctors(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    current_user: User = Depends(get_current_user),
):
    return success_response("Nearby doctors fetched", _STATIC_DOCTORS)
