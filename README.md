# EMA-AI (Python/FastAPI)

## 🚀 Overview

EMA-AI is the AI service of the EMA project, developed in **Python with FastAPI**. It handles adventure generation based on user prompts, using LangChain and OpenAI to create personalized micro-adventure recommendations.

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** (Modern API framework)
- **LangChain** (LLM framework)
- **OpenAI API** (GPT-4 for content generation)
- **Pydantic** (Data validation)
- **Uvicorn** (ASGI server)
- **Docker** (Containerization)

## 📌 Features

- ✅ Adventure generation based on user prompts
- ✅ Semantic search for similar adventures
- ✅ Geolocation-aware recommendations
- ✅ Structured output with consistent format
- ✅ RESTful API with FastAPI
- ✅ Docker setup for easy deployment

## 🏗️ Installation

### **Option 1: Local Development**

#### **1. Clone the repository**

```sh
git clone https://github.com/your-repo/ema-ai.git
cd ema-ai
```

#### **2. Create a virtual environment**

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### **3. Install dependencies**

```sh
pip install -r requirements.txt
```

#### **4. Configure environment variables**

```sh
cp .env.example .env
# Edit .env with your OpenAI API key and other configurations
```

#### **5. Start the server**

```sh
uvicorn main:app --reload --port 8000
```

The API will be accessible at `http://localhost:8000`

### **Option 2: Docker Development**

```sh
# Copy and configure environment variables
cp .env.example .env
# Edit .env with your OpenAI API key and other configurations

# Build and start the container
docker-compose up
```

The API will be accessible at `http://localhost:8000`

## 🔧 Main Endpoints

| Method | Endpoint              | Description                    |
| ------ | --------------------- | ------------------------------ |
| POST   | `/api/generate`       | Generate adventure from prompt |
| POST   | `/api/search_similar` | Find similar adventures        |
| GET    | `/health`             | Check API health status        |
| GET    | `/docs`               | API documentation (Swagger UI) |
| GET    | `/redoc`              | API documentation (ReDoc)      |

## 🔄 Integration with EMA-API

This service is designed to work with the EMA-API (Rails) service. The integration works as follows:

1. EMA-API sends a prompt to this service via HTTP
2. EMA-AI processes the prompt and generates an adventure
3. EMA-AI returns a structured JSON response
4. EMA-API stores the adventure in its database

For detailed integration information, see the [INTEGRATION.md](docs/INTEGRATION.md) document.

## 🧠 Adventure Generation

The adventure generation process uses LangChain and OpenAI to:

1. Parse the user's prompt
2. Extract location, activity preferences, and constraints
3. Generate a suitable adventure with all required fields
4. Format the response in a consistent JSON structure

Example prompt and response:

**Prompt:**

```
Je cherche une randonnée près de Bordeaux
```

**Response:**

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

## 🧪 Tests

To run the tests:

```sh
pytest
```

## 🚀 Deployment

### **Environment Variables**

Make sure to set these environment variables in your production environment:

```
OPENAI_API_KEY=your_openai_api_key
PORT=8000
LOG_LEVEL=info
ALLOWED_ORIGINS=https://your-frontend-domain.com,https://your-api-domain.com
```

### **Deploy with Docker**

```sh
# Build the image
docker build -t ema-ai .

# Run the container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_openai_api_key \
  -e PORT=8000 \
  -e LOG_LEVEL=info \
  -e ALLOWED_ORIGINS=https://your-frontend-domain.com,https://your-api-domain.com \
  ema-ai
```

## 📬 Contributing

Contributions are welcome! Fork the repository and open a PR.

## 📚 Project Structure

```
ema-ai/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── adventure.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── adventure.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── adventure_generator.py
│   │   └── similarity_search.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_adventure_generator.py
│   └── test_routes.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── main.py
├── README.md
└── requirements.txt
```

## 📝 License

MIT License.

## 💬 Contact

Email: `ismael.jouhari@gmail.com`
