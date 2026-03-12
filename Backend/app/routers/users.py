from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

# In-memory store — replace with DB later
_users: List[dict] = []
_id_counter = 1


@router.get("/", response_model=List[UserResponse], summary="List all users")
def list_users():
    return _users


@router.post("/", response_model=UserResponse, status_code=201, summary="Create a user")
def create_user(payload: UserCreate):
    global _id_counter
    user = {"id": _id_counter, **payload.model_dump()}
    _users.append(user)
    _id_counter += 1
    return user


@router.get("/{user_id}", response_model=UserResponse, summary="Get user by ID")
def get_user(user_id: int):
    user = next((u for u in _users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
