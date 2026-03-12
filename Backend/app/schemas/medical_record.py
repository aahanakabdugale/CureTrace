import uuid
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List, Any


class MedicalRecordCreate(BaseModel):
    record_date: Optional[date] = None
    doctor_name: Optional[str] = None
    diagnosis: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None
    attachments: Optional[List[Any]] = []


class MedicalRecordResponse(BaseModel):
    id: uuid.UUID
    patient_id: uuid.UUID
    record_date: Optional[date]
    doctor_name: Optional[str]
    diagnosis: Optional[str]
    prescription: Optional[str]
    notes: Optional[str]
    attachments: List[Any]
    created_at: datetime

    model_config = {"from_attributes": True}
