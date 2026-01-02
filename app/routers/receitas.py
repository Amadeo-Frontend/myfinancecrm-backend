from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models import Receita, User
from app.schemas.receita import ReceitaCreate, ReceitaOut

router = APIRouter(prefix="/receitas", tags=["Receitas"])


@router.post("", response_model=ReceitaOut)
def create_receita(
    payload: ReceitaCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    receita = Receita(
        user_id=user.id,
        descricao=payload.descricao,
        valor=payload.valor,
        categoria=payload.categoria,
        data=payload.data,
    )

    db.add(receita)
    db.commit()
    db.refresh(receita)

    return receita


@router.get("", response_model=list[ReceitaOut])
def list_receitas(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = db.query(Receita).filter(Receita.user_id == user.id)

    if start_date:
        query = query.filter(Receita.data >= start_date)
    if end_date:
        query = query.filter(Receita.data <= end_date)

    return query.order_by(Receita.data.desc()).all()
