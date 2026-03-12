import os
import uuid
import qrcode
from datetime import datetime, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.config import settings

ALGORITHM = "HS256"
QR_DIR = "static/qrcodes"

os.makedirs(QR_DIR, exist_ok=True)


def generate_token(patient_id: uuid.UUID) -> str:
    """Create a signed JWT embedding the patient_id."""
    payload = {
        "sub": str(patient_id),
        "iat": datetime.now(tz=timezone.utc).timestamp(),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_token(token: str) -> uuid.UUID:
    """Verify the token and return the patient_id, or raise 401."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        patient_id = payload.get("sub")
        if not patient_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return uuid.UUID(patient_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired QR token",
        )


def generate_qr_image(patient_id: uuid.UUID, token: str) -> str:
    """
    Generate a QR code PNG that encodes the scan URL.
    Returns the relative file path, e.g. 'static/qrcodes/<uuid>.png'.
    """
    scan_url = f"{settings.qr_base_url}/api/v1/scan/{token}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(scan_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    file_path = os.path.join(QR_DIR, f"{patient_id}.png")
    img.save(file_path)

    return file_path


def qr_image_url(qr_image_path: str) -> str:
    """Convert a local file path to a publicly accessible URL."""
    # e.g. static/qrcodes/uuid.png → http://host/static/qrcodes/uuid.png
    relative = qr_image_path.replace("\\", "/")
    return f"{settings.qr_base_url}/{relative}"
