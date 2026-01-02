from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.core.config import settings

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
        )
        email: str | None = payload.get("email")

        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 🔥 COMO É SÓ VOCÊ, GARANTIMOS UM ÚNICO USER
    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            name="Amadeo",
            email=email,
            role="admin",
            password_hash="nextauth",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
