import uuid
from datetime import date, datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class PatientCreate(BaseModel):
    full_name: str
    dob: date
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class PatientResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    dob: date
    gender: Optional[str]
    blood_type: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
