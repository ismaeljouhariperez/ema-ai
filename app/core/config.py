from pydantic import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Settings(BaseSettings):
    # Paramètres du projet
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "EMA-AI")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "AI service for generating adventure recommendations")
    VERSION: str = os.getenv("VERSION", "0.1.0")
    
    # Paramètres de l'API
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    
    # Paramètres OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instance des paramètres à utiliser dans l'application
settings = Settings() 