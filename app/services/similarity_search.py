from app.models.adventure import SimilarAdventure, SimilarAdventuresResponse
from loguru import logger
from typing import List

class SimilaritySearch:
    """
    Service pour rechercher des aventures similaires
    
    Note: Pour le MVP, cette classe simule la recherche de similarité.
    Dans une version future, elle pourrait utiliser des embeddings et une base vectorielle.
    """
    
    def __init__(self):
        # Simuler une base de données d'aventures pour le MVP
        self.mock_adventures = {
            1: {"id": 1, "title": "Randonnée dans les vignobles de Saint-Émilion"},
            2: {"id": 2, "title": "Balade en kayak sur la Dordogne"},
            3: {"id": 3, "title": "Balade dans les vignes de Pomerol"},
            4: {"id": 4, "title": "Randonnée côtière à Biarritz"},
            5: {"id": 5, "title": "Escalade dans les Pyrénées"},
            6: {"id": 6, "title": "Vélo dans la vallée de la Loire"},
            7: {"id": 7, "title": "Découverte du patrimoine viticole de Fronsac"},
        }
        
        # Simuler des relations de similarité pour le MVP
        self.mock_similarities = {
            1: [3, 7],  # Aventure 1 est similaire aux aventures 3 et 7
            2: [4, 6],
            3: [1, 7],
            4: [2, 5],
            5: [4],
            6: [2],
            7: [1, 3],
        }
    
    async def find_similar_adventures(self, adventure_id: int) -> SimilarAdventuresResponse:
        """
        Trouve des aventures similaires à une aventure donnée
        
        Args:
            adventure_id: L'ID de l'aventure pour laquelle chercher des similaires
            
        Returns:
            Un objet SimilarAdventuresResponse contenant la liste des aventures similaires
        """
        logger.info(f"Recherche d'aventures similaires pour l'ID: {adventure_id}")
        
        # Vérifier si l'aventure existe
        if adventure_id not in self.mock_adventures:
            logger.warning(f"Aventure avec ID {adventure_id} non trouvée")
            return SimilarAdventuresResponse(similar_adventures=[])
        
        # Récupérer les IDs des aventures similaires
        similar_ids = self.mock_similarities.get(adventure_id, [])
        
        # Créer la liste des aventures similaires
        similar_adventures: List[SimilarAdventure] = []
        
        for idx, similar_id in enumerate(similar_ids):
            # Simuler un score de similarité décroissant
            similarity_score = 0.9 - (idx * 0.1)
            
            # Créer l'objet SimilarAdventure
            similar_adventure = SimilarAdventure(
                id=similar_id,
                title=self.mock_adventures[similar_id]["title"],
                similarity_score=similarity_score
            )
            
            similar_adventures.append(similar_adventure)
        
        logger.info(f"Trouvé {len(similar_adventures)} aventures similaires")
        
        # Retourner la réponse
        return SimilarAdventuresResponse(similar_adventures=similar_adventures) 