from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import receitas, despesas, dashboard, me, health

app = FastAPI(title="MyFinanceCRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(receitas.router, prefix="/receitas", tags=["Receitas"])
app.include_router(despesas.router, prefix="/despesas", tags=["Despesas"])
app.include_router(me.router, prefix="/me", tags=["Me"])
