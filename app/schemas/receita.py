from datetime import date
from pydantic import BaseModel


class ReceitaCreate(BaseModel):
    descricao: str
    valor: float
    categoria: str
    data: date


class ReceitaOut(BaseModel):
    id: str
    descricao: str
    valor: float
    categoria: str
    data: date
