import pytest
from unittest.mock import patch, MagicMock
from app.services.adventure_generator import AdventureGenerator
from app.models.adventure import Adventure

@pytest.mark.asyncio
async def test_adventure_generator_mock():
    """Tester le générateur d'aventures avec un mock"""
    
    # Créer une aventure de test
    mock_adventure = Adventure(
        title="Randonnée dans les vignobles de Saint-Émilion",
        description="Une belle balade à travers les célèbres vignobles de Saint-Émilion, offrant des vues panoramiques sur la campagne bordelaise.",
        location="Saint-Émilion, Bordeaux",
        tags=["randonnée", "vignoble", "nature", "patrimoine"],
        difficulty="facile",
        duration=120,
        distance=8.5,
        latitude=44.8946,
        longitude=-0.1556
    )
    
    # Créer un mock pour la chaîne LLM
    with patch.object(AdventureGenerator, '__init__', return_value=None) as mock_init:
        with patch.object(AdventureGenerator, 'chain') as mock_chain:
            # Configurer le mock pour retourner un résultat JSON
            mock_chain.arun = MagicMock(return_value="""
            {
                "title": "Randonnée dans les vignobles de Saint-Émilion",
                "description": "Une belle balade à travers les célèbres vignobles de Saint-Émilion, offrant des vues panoramiques sur la campagne bordelaise.",
                "location": "Saint-Émilion, Bordeaux",
                "tags": ["randonnée", "vignoble", "nature", "patrimoine"],
                "difficulty": "facile",
                "duration": 120,
                "distance": 8.5,
                "latitude": 44.8946,
                "longitude": -0.1556
            }
            """)
            
            # Configurer le mock pour le parser
            generator = AdventureGenerator()
            generator.parser = MagicMock()
            generator.parser.parse = MagicMock(return_value=mock_adventure)
            
            # Appeler la méthode à tester
            result = await generator.generate_adventure("Je cherche une randonnée près de Bordeaux")
            
            # Vérifier que le résultat est correct
            assert result == mock_adventure
            assert result.title == "Randonnée dans les vignobles de Saint-Émilion"
            assert result.location == "Saint-Émilion, Bordeaux"
            assert "randonnée" in result.tags
            assert result.difficulty == "facile"
            assert result.duration == 120
            assert result.distance == 8.5
            assert result.latitude == 44.8946
            assert result.longitude == -0.1556 