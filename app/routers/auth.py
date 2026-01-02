from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
import bcrypt

from app.schemas.auth import LoginRequest
from app.models.user import User
from app.core.security import create_access_token
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if not bcrypt.checkpw(
        payload.password.encode(),
        user.password_hash.encode()
    ):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
