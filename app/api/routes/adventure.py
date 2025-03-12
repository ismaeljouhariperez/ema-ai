from fastapi import APIRouter, Depends, HTTPException
from app.models.adventure import AdventurePrompt, Adventure, SimilarAdventureRequest, SimilarAdventuresResponse
from app.services.adventure_generator import AdventureGenerator
from app.services.similarity_search import SimilaritySearch
from app.core.exceptions import PromptProcessingError, OpenAIError, InvalidPromptError, AdventureNotFoundError
from loguru import logger

# Créer le router
router = APIRouter(tags=["adventures"])

# Dépendances pour injecter les services
def get_adventure_generator():
    return AdventureGenerator()

def get_similarity_search():
    return SimilaritySearch()

@router.post("/generate", response_model=Adventure, summary="Générer une aventure à partir d'un prompt")
async def generate_adventure(
    prompt: AdventurePrompt,
    generator: AdventureGenerator = Depends(get_adventure_generator)
):
    """
    Génère une aventure personnalisée basée sur le prompt de l'utilisateur.
    
    - **prompt**: Le texte décrivant l'aventure souhaitée
    
    Retourne un objet Adventure contenant tous les détails de l'aventure générée.
    
    Peut lever les exceptions suivantes:
    - 400 Bad Request: Si le prompt est invalide
    - 500 Internal Server Error: Si une erreur se produit lors du traitement
    - 503 Service Unavailable: Si l'API OpenAI est indisponible
    """
    logger.info(f"Requête de génération d'aventure reçue: {prompt.prompt}")
    return await generator.generate_adventure(prompt.prompt)

@router.post("/search_similar", response_model=SimilarAdventuresResponse, summary="Trouver des aventures similaires")
async def search_similar_adventures(
    request: SimilarAdventureRequest,
    similarity_search: SimilaritySearch = Depends(get_similarity_search)
):
    """
    Trouve des aventures similaires à une aventure donnée.
    
    - **adventure_id**: L'ID de l'aventure pour laquelle chercher des similaires
    
    Retourne une liste d'aventures similaires avec leurs scores de similarité.
    
    Peut lever les exceptions suivantes:
    - 404 Not Found: Si l'aventure avec l'ID spécifié n'existe pas
    """
    logger.info(f"Requête de recherche d'aventures similaires reçue pour ID: {request.adventure_id}")
    return await similarity_search.find_similar_adventures(request.adventure_id) 