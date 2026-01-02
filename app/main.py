from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.me import router as me_router
from app.routers.receitas import router as receitas_router

from app.core.config import settings
from app.routers.health import router as health_router

app = FastAPI(title="MYFinanceCRM API", version="0.1.0")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(me_router)
app.include_router(receitas_router)
