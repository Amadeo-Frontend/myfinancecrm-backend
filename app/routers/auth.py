from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.session import get_db
from app.db.models import User
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=422, detail="Email ou senha inválidos")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(hours=8),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
