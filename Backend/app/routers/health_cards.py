import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.health_card import HealthCard
from app.models.patient import Patient
from app.schemas.health_card import HealthCardResponse
from app.services import qr_service

router = APIRouter(prefix="/patients", tags=["Health Cards"])


async def _check_patient(db: AsyncSession, patient_id: uuid.UUID) -> Patient:
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post(
    "/{patient_id}/health-card/generate",
    response_model=HealthCardResponse,
    status_code=201,
    summary="Generate or regenerate a QR health card for a patient",
)
async def generate_health_card(
    patient_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    await _check_patient(db, patient_id)

    # Check for existing card and deactivate it
    result = await db.execute(
        select(HealthCard).where(HealthCard.patient_id == patient_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.is_active = False
        await db.commit()

    # Generate new token + QR image
    token = qr_service.generate_token(patient_id)
    image_path = qr_service.generate_qr_image(patient_id, token)

    card = HealthCard(
        patient_id=patient_id,
        token=token,
        qr_image_path=image_path,
        is_active=True,
    )
    # If there was an existing record, delete it (one card per patient)
    if existing:
        await db.delete(existing)
        await db.commit()

    db.add(card)
    await db.commit()
    await db.refresh(card)

    return HealthCardResponse(
        id=card.id,
        patient_id=card.patient_id,
        qr_image_url=qr_service.qr_image_url(card.qr_image_path),
        is_active=card.is_active,
        issued_at=card.issued_at,
        expires_at=card.expires_at,
    )


@router.get(
    "/{patient_id}/health-card",
    response_model=HealthCardResponse,
    summary="Get the active health card for a patient",
)
async def get_health_card(patient_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await _check_patient(db, patient_id)
    result = await db.execute(
        select(HealthCard).where(
            HealthCard.patient_id == patient_id,
            HealthCard.is_active == True,
        )
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="No active health card found. Generate one first.")
    return HealthCardResponse(
        id=card.id,
        patient_id=card.patient_id,
        qr_image_url=qr_service.qr_image_url(card.qr_image_path),
        is_active=card.is_active,
        issued_at=card.issued_at,
        expires_at=card.expires_at,
    )


@router.delete(
    "/{patient_id}/health-card",
    status_code=204,
    summary="Revoke / deactivate the patient's health card",
)
async def revoke_health_card(patient_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await _check_patient(db, patient_id)
    result = await db.execute(
        select(HealthCard).where(HealthCard.patient_id == patient_id)
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="No health card found for this patient")
    card.is_active = False
    await db.commit()
