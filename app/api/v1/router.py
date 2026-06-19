from fastapi import APIRouter

from app.api.v1.routes import analyses, health, properties, practice

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(properties.router)
api_router.include_router(analyses.router)
api_router.include_router(practice.router)
