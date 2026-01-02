from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == payload.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado",
        )

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role="user",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    return Token(access_token=access_token)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    return Token(access_token=access_token)
