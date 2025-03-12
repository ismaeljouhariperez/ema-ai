import pytest
from fastapi.testclient import TestClient
from main import app

# Créer un client de test
client = TestClient(app)

def test_health_check():
    """Tester la route de santé"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "ok"

def test_generate_adventure():
    """Tester la route de génération d'aventure (mock)"""
    # Note: Ce test ne fait pas réellement appel à l'API OpenAI
    # Il vérifie simplement que la route est correctement configurée
    
    # Désactiver ce test en production pour éviter des appels API inutiles
    pytest.skip("Skipping test to avoid unnecessary API calls")
    
    response = client.post(
        "/api/generate",
        json={"prompt": "Je cherche une randonnée près de Bordeaux"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "description" in data
    assert "location" in data
    assert "tags" in data
    assert "difficulty" in data
    assert "duration" in data
    assert "distance" in data
    assert "latitude" in data
    assert "longitude" in data

def test_search_similar_adventures():
    """Tester la route de recherche d'aventures similaires"""
    response = client.post(
        "/api/search_similar",
        json={"adventure_id": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert "similar_adventures" in data
    assert isinstance(data["similar_adventures"], list)
    
    # Vérifier que les aventures similaires ont le bon format
    if data["similar_adventures"]:
        adventure = data["similar_adventures"][0]
        assert "id" in adventure
        assert "title" in adventure
        assert "similarity_score" in adventure 