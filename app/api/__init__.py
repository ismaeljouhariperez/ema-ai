from fastapi import APIRouter
from app.api.routes import adventure_router

# Créer le router principal
api_router = APIRouter()

# Inclure les sous-routers
api_router.include_router(adventure_router, prefix="/api")

__all__ = ["api_router"]
