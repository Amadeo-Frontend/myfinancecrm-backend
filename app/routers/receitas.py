from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.db.models import Receita, User
from app.schemas.receita import ReceitaCreate, ReceitaOut
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/receitas",
    tags=["Receitas"],
)


@router.post("", response_model=ReceitaOut)
def create_receita(
    data: ReceitaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    receita = Receita(
        user_id=current_user.id,
        descricao=data.descricao,
        valor=data.valor,
        categoria=data.categoria,
        data=data.data,
    )

    db.add(receita)
    db.commit()
    db.refresh(receita)

    return receita


@router.get("", response_model=list[ReceitaOut])
def list_receitas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Receita)
        .filter(Receita.user_id == current_user.id)
        .order_by(Receita.data.desc())
        .all()
    )


@router.get("/{receita_id}", response_model=ReceitaOut)
def get_receita(
    receita_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    receita = (
        db.query(Receita)
        .filter(
            Receita.id == receita_id,
            Receita.user_id == current_user.id,
        )
        .first()
    )

    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")

    return receita


@router.delete("/{receita_id}", status_code=204)
def delete_receita(
    receita_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    receita = (
        db.query(Receita)
        .filter(
            Receita.id == receita_id,
            Receita.user_id == current_user.id,
        )
        .first()
    )

    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")

    db.delete(receita)
    db.commit()
