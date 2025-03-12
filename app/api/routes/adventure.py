from fastapi import APIRouter, Depends, HTTPException
from app.models.adventure import AdventurePrompt, Adventure, SimilarAdventureRequest, SimilarAdventuresResponse
from app.services.adventure_generator import AdventureGenerator
from app.services.similarity_search import SimilaritySearch
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
    """
    try:
        logger.info(f"Requête de génération d'aventure reçue: {prompt.prompt}")
        adventure = await generator.generate_adventure(prompt.prompt)
        return adventure
    except Exception as e:
        logger.error(f"Erreur lors de la génération d'aventure: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération d'aventure: {str(e)}"
        )

@router.post("/search_similar", response_model=SimilarAdventuresResponse, summary="Trouver des aventures similaires")
async def search_similar_adventures(
    request: SimilarAdventureRequest,
    similarity_search: SimilaritySearch = Depends(get_similarity_search)
):
    """
    Trouve des aventures similaires à une aventure donnée.
    
    - **adventure_id**: L'ID de l'aventure pour laquelle chercher des similaires
    
    Retourne une liste d'aventures similaires avec leurs scores de similarité.
    """
    try:
        logger.info(f"Requête de recherche d'aventures similaires reçue pour ID: {request.adventure_id}")
        similar_adventures = await similarity_search.find_similar_adventures(request.adventure_id)
        return similar_adventures
    except Exception as e:
        logger.error(f"Erreur lors de la recherche d'aventures similaires: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la recherche d'aventures similaires: {str(e)}"
        ) 