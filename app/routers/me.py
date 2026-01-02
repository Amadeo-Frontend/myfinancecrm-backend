from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.db.models import User

router = APIRouter(prefix="/me", tags=["Me"])


@router.get("")
def read_me(user: User = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }
