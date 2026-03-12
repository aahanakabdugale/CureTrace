import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


async def create_patient(db: AsyncSession, data: PatientCreate) -> Patient:
    patient = Patient(**data.model_dump())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return patient


async def get_patient(db: AsyncSession, patient_id: uuid.UUID) -> Optional[Patient]:
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    return result.scalar_one_or_none()


async def list_patients(db: AsyncSession) -> list[Patient]:
    result = await db.execute(select(Patient).order_by(Patient.created_at.desc()))
    return list(result.scalars().all())


async def update_patient(
    db: AsyncSession, patient_id: uuid.UUID, data: PatientUpdate
) -> Optional[Patient]:
    changes = {k: v for k, v in data.model_dump().items() if v is not None}
    if not changes:
        return await get_patient(db, patient_id)
    await db.execute(
        update(Patient).where(Patient.id == patient_id).values(**changes)
    )
    await db.commit()
    return await get_patient(db, patient_id)


async def delete_patient(db: AsyncSession, patient_id: uuid.UUID) -> bool:
    patient = await get_patient(db, patient_id)
    if not patient:
        return False
    await db.delete(patient)
    await db.commit()
    return True
