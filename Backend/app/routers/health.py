from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health Check")
def health_check():
    return {
        "status": "ok",
        "service": "CureTrace API",
        "timestamp": datetime.utcnow().isoformat(),
    }
