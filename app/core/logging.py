import sys
import logging
from loguru import logger
from app.core.config import settings

# Configuration de loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Récupérer le message original du record
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

# Configurer le logger
def setup_logging():
    # Supprimer les handlers par défaut
    logger.remove()
    
    # Ajouter un handler pour la sortie standard
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level=settings.LOG_LEVEL.upper(),
        serialize=False,
    )
    
    # Intercepter les logs de uvicorn et fastapi
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    
    # Configurer les loggers spécifiques
    for _log in ["uvicorn", "uvicorn.access", "fastapi"]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]
        
    return logger 