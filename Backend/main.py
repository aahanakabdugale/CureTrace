from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, users

app = FastAPI(
    title="CureTrace API",
    description="Backend API for CureTrace application",
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

# Routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to CureTrace API 🚀"}
