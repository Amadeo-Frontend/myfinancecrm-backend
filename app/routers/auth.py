from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.core.security import (
    verify_password,
    create_access_token,
    get_password_hash
)
from app.schemas.user import UserCreate, Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == payload.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    user = User(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role="user",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=422, detail="Email ou senha inválidos")

    token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    return {"access_token": token, "token_type": "bearer"}
