from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.db.session import get_db
from app.db.models import Receita, Despesa, User
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_receitas = (
        db.query(func.coalesce(func.sum(Receita.valor), 0))
        .filter(Receita.user_id == current_user.id)
        .scalar()
    )

    total_despesas = (
        db.query(func.coalesce(func.sum(Despesa.valor), 0))
        .filter(Despesa.user_id == current_user.id)
        .scalar()
    )

    return {
        "total_receitas": float(total_receitas),
        "total_despesas": float(total_despesas),
        "saldo": float(total_receitas - total_despesas),
    }
