import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.patient import PatientResponse
from app.schemas.medical_record import MedicalRecordResponse


class HealthCardResponse(BaseModel):
    id: uuid.UUID
    patient_id: uuid.UUID
    qr_image_url: str
    is_active: bool
    issued_at: datetime
    expires_at: Optional[datetime]

    model_config = {"from_attributes": True}


class ScannedRecordResponse(BaseModel):
    """Full bundle returned when a QR code is scanned."""
    patient: PatientResponse
    medical_records: List[MedicalRecordResponse]
