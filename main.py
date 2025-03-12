import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging

# Configurer le logger
logger = setup_logging()

# Créer l'application FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes API
app.include_router(api_router)

# Route de santé
@app.get("/health", tags=["health"])
async def health_check():
    """
    Vérifier que l'API est en ligne
    """
    return {"status": "ok", "version": settings.VERSION}

# Point d'entrée pour exécuter l'application directement
if __name__ == "__main__":
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower(),
    ) 