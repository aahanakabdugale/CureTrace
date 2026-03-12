import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.services import patient_service

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/", response_model=PatientResponse, status_code=201, summary="Register a new patient")
async def create_patient(payload: PatientCreate, db: AsyncSession = Depends(get_db)):
    return await patient_service.create_patient(db, payload)


@router.get("/", response_model=List[PatientResponse], summary="List all patients")
async def list_patients(db: AsyncSession = Depends(get_db)):
    return await patient_service.list_patients(db)


@router.get("/{patient_id}", response_model=PatientResponse, summary="Get patient by ID")
async def get_patient(patient_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    patient = await patient_service.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.patch("/{patient_id}", response_model=PatientResponse, summary="Update patient fields")
async def update_patient(
    patient_id: uuid.UUID, payload: PatientUpdate, db: AsyncSession = Depends(get_db)
):
    patient = await patient_service.update_patient(db, patient_id, payload)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.delete("/{patient_id}", status_code=204, summary="Delete a patient")
async def delete_patient(patient_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    deleted = await patient_service.delete_patient(db, patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
