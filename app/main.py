from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.auth import router as auth_router
from app.routers.me import router as me_router
from app.routers.receitas import router as receitas_router
from app.routers.despesas import router as despesas_router
from app.routers.dashboard import router as dashboard_router
from app.routers.health import router as health_router

from app.db.migrate import run_migrations

app = FastAPI(
    title="MYFinanceCRM API",
    version="0.1.0",
)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 roda migrations automaticamente no Render
@app.on_event("startup")
def startup_event():
    run_migrations()

# Routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(me_router)
app.include_router(receitas_router)
app.include_router(despesas_router)
app.include_router(dashboard_router)
