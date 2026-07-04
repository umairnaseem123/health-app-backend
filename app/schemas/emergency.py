"""
Pydantic schema for the nearby-doctors endpoint.
"""
from pydantic import BaseModel


class DoctorOut(BaseModel):
    id: int
    name: str
    specialty: str
    hospital: str
    address: str
    phone: str
    distance_km: float
