from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.health_card import HealthCard
from app.models.patient import Patient
from app.models.medical_record import MedicalRecord
from app.schemas.health_card import ScannedRecordResponse
from app.schemas.patient import PatientResponse
from app.schemas.medical_record import MedicalRecordResponse
from app.services import qr_service

router = APIRouter(tags=["QR Scan"])


@router.get(
    "/scan/{token}",
    response_model=ScannedRecordResponse,
    summary="Scan QR — returns full patient record bundle (public endpoint)",
)
async def scan_qr(token: str, db: AsyncSession = Depends(get_db)):
    # 1. Decode + verify JWT token
    patient_id = qr_service.decode_token(token)

    # 2. Check the card is still active (not revoked)
    card_result = await db.execute(
        select(HealthCard).where(
            HealthCard.patient_id == patient_id,
            HealthCard.token == token,
        )
    )
    card = card_result.scalar_one_or_none()
    if not card or not card.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This QR code has been revoked or is no longer valid",
        )

    # 3. Fetch patient
    patient_result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = patient_result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # 4. Fetch medical records
    records_result = await db.execute(
        select(MedicalRecord)
        .where(MedicalRecord.patient_id == patient_id)
        .order_by(MedicalRecord.created_at.desc())
    )
    records = list(records_result.scalars().all())

    return ScannedRecordResponse(
        patient=PatientResponse.model_validate(patient),
        medical_records=[MedicalRecordResponse.model_validate(r) for r in records],
    )
