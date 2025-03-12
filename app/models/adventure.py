from pydantic import BaseModel, Field
from typing import List, Optional

class AdventurePrompt(BaseModel):
    """Modèle pour la requête de génération d'aventure"""
    prompt: str = Field(..., description="Prompt utilisateur décrivant l'aventure souhaitée")

class Adventure(BaseModel):
    """Modèle pour une aventure générée"""
    title: str = Field(..., description="Titre de l'aventure")
    description: str = Field(..., description="Description détaillée de l'aventure")
    location: str = Field(..., description="Lieu de l'aventure")
    tags: List[str] = Field(..., description="Tags associés à l'aventure")
    difficulty: str = Field(..., description="Niveau de difficulté (facile, moyen, difficile)")
    duration: int = Field(..., description="Durée estimée en minutes")
    distance: float = Field(..., description="Distance en kilomètres")
    latitude: float = Field(..., description="Latitude du point de départ")
    longitude: float = Field(..., description="Longitude du point de départ")

class SimilarAdventureRequest(BaseModel):
    """Modèle pour la requête de recherche d'aventures similaires"""
    adventure_id: int = Field(..., description="ID de l'aventure pour laquelle chercher des similaires")

class SimilarAdventure(BaseModel):
    """Modèle pour une aventure similaire"""
    id: int = Field(..., description="ID de l'aventure similaire")
    title: str = Field(..., description="Titre de l'aventure similaire")
    similarity_score: float = Field(..., description="Score de similarité (0-1)")

class SimilarAdventuresResponse(BaseModel):
    """Modèle pour la réponse de recherche d'aventures similaires"""
    similar_adventures: List[SimilarAdventure] = Field(..., description="Liste des aventures similaires") 