#!/usr/bin/env python3
"""
API REST FastAPI pour le Générateur de Prompts No Code
=======================================================
Serveur production-ready avec documentation auto-générée
"""

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
import logging
from datetime import datetime
import time

from prompt_generator import generate_from_text, PromptStructure

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialisation de l'application
app = FastAPI(
    title="Prompt Maître API",
    description="API de génération automatique de prompts optimisés pour No Code",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS pour permettre les appels depuis Make, n8n, Bubble
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modèles Pydantic pour validation
class PromptRequest(BaseModel):
    """Requête de génération de prompt"""
    raw_text: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Texte brut décrivant le besoin d'automatisation",
        example="Je veux connecter Airtable à Slack pour être notifié quand un nouvel enregistrement est ajouté."
    )
    options: Optional[Dict] = Field(
        default={},
        description="Options avancées (réservé pour extensions futures)"
    )

    @validator('raw_text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("Le texte ne peut pas être vide")
        return v.strip()


class PromptResponse(BaseModel):
    """Réponse avec le prompt généré"""
    text_prompt: str = Field(..., description="Prompt optimisé au format texte markdown")
    json_prompt: str = Field(..., description="Prompt structuré au format JSON")
    metadata: Dict = Field(..., description="Métadonnées sur la génération")


class HealthResponse(BaseModel):
    """Réponse du health check"""
    status: str
    timestamp: str
    version: str


class ErrorResponse(BaseModel):
    """Réponse d'erreur standardisée"""
    error: str
    detail: str
    timestamp: str


# Middleware pour logging des requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log toutes les requêtes avec leur durée"""
    start_time = time.time()

    # Log de la requête entrante
    logger.info(f"Incoming request: {request.method} {request.url.path}")

    response = await call_next(request)

    # Calculer la durée
    duration = time.time() - start_time
    logger.info(f"Request completed in {duration:.3f}s with status {response.status_code}")

    return response


# Routes
@app.get("/", tags=["Root"])
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API Prompt Maître",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health",
        "generate_endpoint": "/generate"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Vérifie l'état de santé de l'API"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post(
    "/generate",
    response_model=PromptResponse,
    responses={
        200: {"description": "Prompt généré avec succès"},
        400: {"description": "Requête invalide", "model": ErrorResponse},
        500: {"description": "Erreur serveur", "model": ErrorResponse}
    },
    tags=["Generation"]
)
async def generate_prompt(request: PromptRequest):
    """
    Génère un prompt optimisé à partir d'un texte brut

    **Paramètres:**
    - **raw_text**: Description du besoin d'automatisation (10-5000 caractères)

    **Retour:**
    - **text_prompt**: Prompt au format texte markdown, lisible et structuré
    - **json_prompt**: Même prompt au format JSON standardisé
    - **metadata**: Informations sur le traitement (temps, complexité, etc.)

    **Exemples de textes d'entrée:**
    - "Je veux connecter Airtable à Slack"
    - "Automatiser l'envoi d'emails depuis Google Sheets"
    - "Créer un workflow avec OpenAI pour analyser des feedbacks"
    """
    try:
        start_time = time.time()

        logger.info(f"Generating prompt for text: {request.raw_text[:50]}...")

        # Générer le prompt
        result = generate_from_text(request.raw_text)

        # Calculer le temps de génération
        generation_time = time.time() - start_time

        # Extraire les métadonnées de l'analyse
        analysis = result["analysis"]

        metadata = {
            "generation_time_seconds": round(generation_time, 3),
            "input_length": len(request.raw_text),
            "output_length_text": len(result["text_prompt"]),
            "output_length_json": len(result["json_prompt"]),
            "detected_tools": analysis.tools,
            "detected_intent": analysis.intent,
            "complexity_score": analysis.complexity_score,
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"Prompt generated successfully in {generation_time:.3f}s")

        return PromptResponse(
            text_prompt=result["text_prompt"],
            json_prompt=result["json_prompt"],
            metadata=metadata
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du prompt: {str(e)}"
        )


@app.post("/batch", tags=["Generation"])
async def generate_batch(requests: List[PromptRequest]):
    """
    Génère plusieurs prompts en batch

    **Limite:** 10 requêtes par batch
    """
    if len(requests) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 requêtes par batch"
        )

    results = []
    for req in requests:
        try:
            result = generate_from_text(req.raw_text)
            results.append({
                "status": "success",
                "text_prompt": result["text_prompt"],
                "json_prompt": result["json_prompt"]
            })
        except Exception as e:
            results.append({
                "status": "error",
                "error": str(e)
            })

    return {"results": results}


@app.get("/tools", tags=["Info"])
async def list_supported_tools():
    """Liste les outils No Code reconnus par le générateur"""
    return {
        "supported_tools": [
            "Make.com",
            "Zapier",
            "n8n",
            "Airtable",
            "Notion",
            "Bubble",
            "Slack",
            "Google Sheets",
            "Webhooks",
            "API",
            "OpenAI",
            "Anthropic Claude"
        ],
        "total": 12
    }


@app.get("/intents", tags=["Info"])
async def list_supported_intents():
    """Liste les intentions détectables par le générateur"""
    return {
        "supported_intents": [
            {"name": "connexion", "keywords": ["connecter", "relier", "lier"]},
            {"name": "automatisation", "keywords": ["automatiser", "déclencher"]},
            {"name": "notification", "keywords": ["notifier", "alerter", "prévenir"]},
            {"name": "création", "keywords": ["créer", "ajouter", "générer"]},
            {"name": "mise à jour", "keywords": ["mettre à jour", "modifier"]},
            {"name": "synchronisation", "keywords": ["synchroniser", "synchro"]},
            {"name": "transformation", "keywords": ["transformer", "convertir"]},
            {"name": "filtrage", "keywords": ["filtrer", "trier"]},
            {"name": "analyse", "keywords": ["analyser", "examiner"]},
            {"name": "génération", "keywords": ["générer", "produire"]}
        ]
    }


@app.get("/schema", tags=["Info"])
async def get_json_schema():
    """Retourne le schéma JSON de sortie"""
    return {
        "schema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["role", "objective", "context", "tools", "instructions", "output_format", "tone"],
            "properties": {
                "role": {"type": "string"},
                "objective": {"type": "string"},
                "context": {"type": "string"},
                "tools": {"type": "array", "items": {"type": "string"}},
                "instructions": {"type": "array", "items": {"type": "string"}},
                "output_format": {"type": "string"},
                "tone": {"type": "string"},
                "constraints": {"type": "array", "items": {"type": "string"}},
                "examples": {"type": "array", "items": {"type": "string"}}
            }
        }
    }


@app.get("/examples", tags=["Info"])
async def get_examples():
    """Retourne des exemples d'utilisation"""
    return {
        "examples": [
            {
                "input": "Je veux connecter Airtable à Slack pour être notifié quand un nouvel enregistrement est ajouté.",
                "description": "Connexion simple entre deux outils",
                "complexity": 2
            },
            {
                "input": "Créer une automatisation qui récupère les nouveaux leads depuis Google Sheets, vérifie leur validité avec une API, enrichit les données via OpenAI, puis crée un enregistrement dans Airtable.",
                "description": "Workflow complexe multi-étapes avec IA",
                "complexity": 5
            },
            {
                "input": "Synchroniser automatiquement les tâches entre Notion et Airtable dans les deux sens.",
                "description": "Synchronisation bidirectionnelle",
                "complexity": 4
            }
        ]
    }


# Gestionnaire d'erreurs global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Gère toutes les exceptions non capturées"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            detail=str(exc),
            timestamp=datetime.now().isoformat()
        ).dict()
    )


# Point d'entrée pour exécution directe
if __name__ == "__main__":
    import uvicorn

    print("=" * 80)
    print("🚀 Démarrage de l'API Prompt Maître")
    print("=" * 80)
    print("\n📍 L'API sera accessible sur : http://localhost:8000")
    print("📚 Documentation interactive : http://localhost:8000/docs")
    print("📖 Documentation alternative : http://localhost:8000/redoc")
    print("\n" + "=" * 80 + "\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
