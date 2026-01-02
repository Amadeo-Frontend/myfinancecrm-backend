from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


class DespesaCreate(BaseModel):
    descricao: str
    valor: Decimal
    categoria: str
    data: date


class DespesaOut(BaseModel):
    id: UUID
    descricao: str
    valor: Decimal
    categoria: str
    data: date
    created_at: datetime

    class Config:
        from_attributes = True
