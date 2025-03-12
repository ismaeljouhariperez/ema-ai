# Intégration EMA-API et EMA-AI

Ce document décrit l'intégration entre les services `ema-api` (Rails 8) et `ema-ai` (Python/FastAPI).

## Architecture globale

L'écosystème EMA est composé de trois services principaux :

1. **ema-api** (Rails 8) - Ce repository

   - Gère les utilisateurs, l'authentification, le stockage des aventures
   - Expose une API REST pour le frontend
   - Communique avec ema-ai pour la génération d'aventures

2. **ema-ai** (Python/FastAPI)

   - Utilise LangChain et OpenAI pour le traitement IA
   - Génère des recommandations d'aventures basées sur les prompts utilisateurs
   - Expose une API REST consommée par ema-api

3. **ema-frontend** (React/TypeScript)
   - Interface utilisateur
   - Communique uniquement avec ema-api

## Points d'intégration

### Communication ema-api → ema-ai

Le service ema-api communique avec ema-ai via HTTP en utilisant la bibliothèque Faraday :

```ruby
# app/services/ema_ai_service.rb
class EmaAiService
  def initialize
    @api_url = ENV['EMA_AI_API_URL'] || 'http://localhost:8000'
  end

  def generate_adventure(prompt)
    response = Faraday.post("#{@api_url}/api/generate") do |req|
      req.headers['Content-Type'] = 'application/json'
      req.body = { prompt: prompt }.to_json
    end

    JSON.parse(response.body)
  end
end
```

### Traitement asynchrone

La génération d'aventures est traitée de manière asynchrone avec Sidekiq :

```ruby
# app/controllers/api/v1/ai_adventures_controller.rb
def generate
  job = GenerateAdventureJob.perform_later(current_user.id, params[:prompt])
  render json: { job_id: job.provider_job_id, status: 'processing' }
end

# app/jobs/generate_adventure_job.rb
class GenerateAdventureJob < ApplicationJob
  queue_as :default

  def perform(user_id, prompt)
    user = User.find(user_id)
    service = EmaAiService.new
    adventure_data = service.generate_adventure(prompt)

    # Création de l'aventure à partir des données générées
    adventure = Adventure.new(
      title: adventure_data['title'],
      description: adventure_data['description'],
      location: adventure_data['location'],
      tags: adventure_data['tags'].join(','),
      difficulty: adventure_data['difficulty'],
      duration: adventure_data['duration'],
      distance: adventure_data['distance'],
      user: user
    )

    adventure.save!
    adventure
  end
end
```

## API attendue de ema-ai

Le service ema-ai doit exposer les endpoints suivants :

### Générer une aventure

**Endpoint** : `POST /api/generate`

**Payload** :

```json
{
  "prompt": "Je cherche une randonnée près de Bordeaux"
}
```

**Réponse attendue** :

```json
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
```

### Rechercher des aventures similaires

**Endpoint** : `POST /api/search_similar`

**Payload** :

```json
{
  "adventure_id": 1
}
```

**Réponse attendue** :

```json
{
  "similar_adventures": [
    {
      "id": 3,
      "title": "Balade dans les vignes de Pomerol",
      "similarity_score": 0.89
    },
    {
      "id": 7,
      "title": "Découverte du patrimoine viticole de Fronsac",
      "similarity_score": 0.76
    }
  ]
}
```

## Configuration requise

### Variables d'environnement

Dans ema-api, configurez la variable d'environnement suivante :

```
EMA_AI_API_URL=http://localhost:8000  # URL du service ema-ai
```

Dans ema-ai, configurez les variables d'environnement suivantes :

```
OPENAI_API_KEY=your_openai_api_key  # Clé API OpenAI
PORT=8000                           # Port d'écoute (doit correspondre à EMA_AI_API_URL)
```

### Prérequis pour le développement local

Pour tester l'intégration localement :

1. Démarrez Redis (requis par Sidekiq) :

   ```bash
   brew services start redis  # macOS avec Homebrew
   ```

2. Démarrez Sidekiq dans ema-api :

   ```bash
   bundle exec sidekiq
   ```

3. Démarrez le serveur ema-api :

   ```bash
   rails s
   ```

4. Démarrez le serveur ema-ai :
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## Tests d'intégration

Pour tester l'intégration entre les deux services, vous pouvez utiliser les commandes curl suivantes :

```bash
# 1. Créer un utilisateur
curl -X POST -H "Content-Type: application/json" -d '{
  "email": "test@example.com",
  "password": "password123",
  "password_confirmation": "password123",
  "name": "Test User"
}' http://localhost:3000/auth

# 2. Se connecter pour obtenir les jetons d'authentification
curl -i -X POST -H "Content-Type: application/json" -d '{
  "email": "test@example.com",
  "password": "password123"
}' http://localhost:3000/auth/sign_in

# 3. Générer une aventure avec l'IA (remplacer les jetons par ceux obtenus à l'étape 2)
curl -X POST -H "Content-Type: application/json" \
  -H "access-token: <VOTRE_ACCESS_TOKEN>" \
  -H "client: <VOTRE_CLIENT_ID>" \
  -H "uid: <VOTRE_EMAIL>" \
  -d '{
    "prompt": "Je cherche une randonnée près de Bordeaux"
  }' http://localhost:3000/api/v1/ai_adventures/generate
```

Pour plus de détails sur les tests API, consultez [API_TESTING.md](API_TESTING.md).

## Documentation complète

Pour une documentation plus détaillée :

- **ema-api** : Voir [DEVELOPMENT.md](DEVELOPMENT.md) et [TECHNICAL.md](TECHNICAL.md)
- **ema-ai** : Consultez la documentation dans le repository correspondant
