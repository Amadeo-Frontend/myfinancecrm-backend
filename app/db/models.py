from sqlalchemy import (
    Column,
    String,
    Text,
    Date,
    Numeric,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid

from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    receitas = relationship("Receita", back_populates="user", cascade="all, delete")
    despesas = relationship("Despesa", back_populates="user", cascade="all, delete")


class Receita(Base):
    __tablename__ = "receitas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    descricao = Column(Text)
    valor = Column(Numeric(12, 2), nullable=False)
    categoria = Column(String(100))
    data = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="receitas")


class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    descricao = Column(Text)
    valor = Column(Numeric(12, 2), nullable=False)
    categoria = Column(String(100))
    data = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="despesas")
