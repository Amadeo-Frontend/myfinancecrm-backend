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

app = FastAPI(
    title="MyFinanceCRM API",
    version="1.0.0",
)

# 🔥 Cria as tabelas no startup (ok para dev / projeto pessoal)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# 🌐 CORS (frontend Next.js + Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://myfinancecrm-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Routers (TODOS PROTEGIDOS VIA Bearer Token)
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(me_router, prefix="/me", tags=["Me"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(receitas_router, prefix="/receitas", tags=["Receitas"])
app.include_router(despesas_router, prefix="/despesas", tags=["Despesas"])


@app.get("/")
def root():
    return {"status": "ok"}
