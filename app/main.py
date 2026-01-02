from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.db.models import Base

from app.routers.dashboard import router as dashboard_router
from app.routers.receitas import router as receitas_router
from app.routers.despesas import router as despesas_router
from app.routers.me import router as me_router
from app.routers.health import router as health_router

app = FastAPI(title="MyFinanceCRM API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(receitas_router, prefix="/receitas", tags=["Receitas"])
app.include_router(despesas_router, prefix="/despesas", tags=["Despesas"])
app.include_router(me_router, prefix="/me", tags=["Me"])
app.include_router(health_router, prefix="/health", tags=["Health"])
