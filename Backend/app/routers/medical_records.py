import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.medical_record import MedicalRecord
from app.models.patient import Patient
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordResponse

router = APIRouter(prefix="/patients", tags=["Medical Records"])


async def _check_patient(db: AsyncSession, patient_id: uuid.UUID) -> Patient:
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post(
    "/{patient_id}/records/",
    response_model=MedicalRecordResponse,
    status_code=201,
    summary="Add a medical record for a patient",
)
async def add_record(
    patient_id: uuid.UUID,
    payload: MedicalRecordCreate,
    db: AsyncSession = Depends(get_db),
):
    await _check_patient(db, patient_id)
    record = MedicalRecord(patient_id=patient_id, **payload.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


@router.get(
    "/{patient_id}/records/",
    response_model=List[MedicalRecordResponse],
    summary="List all medical records for a patient",
)
async def list_records(patient_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await _check_patient(db, patient_id)
    result = await db.execute(
        select(MedicalRecord)
        .where(MedicalRecord.patient_id == patient_id)
        .order_by(MedicalRecord.created_at.desc())
    )
    return list(result.scalars().all())


@router.get(
    "/{patient_id}/records/{record_id}",
    response_model=MedicalRecordResponse,
    summary="Get a single medical record",
)
async def get_record(
    patient_id: uuid.UUID, record_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MedicalRecord).where(
            MedicalRecord.id == record_id,
            MedicalRecord.patient_id == patient_id,
        )
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record


@router.delete(
    "/{patient_id}/records/{record_id}",
    status_code=204,
    summary="Delete a medical record",
)
async def delete_record(
    patient_id: uuid.UUID, record_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MedicalRecord).where(
            MedicalRecord.id == record_id,
            MedicalRecord.patient_id == patient_id,
        )
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    await db.delete(record)
    await db.commit()
