from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.db.models import Despesa, User
from app.schemas.despesa import DespesaCreate, DespesaOut
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/despesas",
    tags=["Despesas"],
)


@router.post("", response_model=DespesaOut)
def create_despesa(
    data: DespesaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    despesa = Despesa(
        user_id=current_user.id,
        descricao=data.descricao,
        valor=data.valor,
        categoria=data.categoria,
        data=data.data,
    )

    db.add(despesa)
    db.commit()
    db.refresh(despesa)

    return despesa


@router.get("", response_model=list[DespesaOut])
def list_despesas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Despesa)
        .filter(Despesa.user_id == current_user.id)
        .order_by(Despesa.data.desc())
        .all()
    )


@router.delete("/{despesa_id}", status_code=204)
def delete_despesa(
    despesa_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    despesa = (
        db.query(Despesa)
        .filter(
            Despesa.id == despesa_id,
            Despesa.user_id == current_user.id,
        )
        .first()
    )

    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa nao encontrada")

    db.delete(despesa)
    db.commit()
