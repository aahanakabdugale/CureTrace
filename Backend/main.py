from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.routers import health, users, patients, medical_records, health_cards, scan

app = FastAPI(
    title="CureTrace API",
    description="Backend API for CureTrace — QR-Based Smart Health Card system",
    version="1.0.0",
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated QR code images
os.makedirs("static/qrcodes", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── Routers ────────────────────────────────────────────────
app.include_router(health.router,          prefix="/api/v1")
app.include_router(users.router,           prefix="/api/v1")
app.include_router(patients.router,        prefix="/api/v1")
app.include_router(medical_records.router, prefix="/api/v1")
app.include_router(health_cards.router,    prefix="/api/v1")
app.include_router(scan.router,            prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to CureTrace API 🚀"}
