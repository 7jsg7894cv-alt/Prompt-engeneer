# 🔌 Intégrations No Code pour le Générateur de Prompts

Guide complet pour implémenter le générateur dans les plateformes No Code populaires.

---

## 📦 Make.com (Integromat)

### Architecture du scénario

```
[Webhook] → [HTTP Request: Python Script] → [JSON Parser] → [Router] → [Text Formatter]
                                                                      → [Data Store]
```

### Configuration détaillée

#### Module 1 : Webhook (Déclencheur)
- Type : **Custom Webhook**
- Method : POST
- Content-Type : application/json
- Body structure :
```json
{
  "raw_text": "Votre texte brut ici"
}
```

#### Module 2 : HTTP Request (Appel API Python)
- URL : `https://votre-serveur.com/generate-prompt`
- Method : POST
- Headers :
  - Content-Type: application/json
- Body :
```json
{
  "raw_text": "{{1.raw_text}}"
}
```

**Option Alternative** : Exécuter le script Python directement
- Utiliser un serveur AWS Lambda, Google Cloud Functions, ou Azure Functions
- Déployer `prompt_generator.py` comme fonction serverless
- Endpoint : `/generate`

#### Module 3 : JSON Parser
- Parse le résultat de la requête HTTP
- Extraction des champs :
  - `text_prompt`
  - `json_prompt`

#### Module 4 : Router (Sortie multiple)
- **Route 1** : Enregistrer dans Google Sheets / Airtable
- **Route 2** : Envoyer par email / Slack
- **Route 3** : Webhook de réponse

#### Module 5a : Text Formatter (Route 1)
- Format : Markdown → HTML ou Plain Text
- Destination : Email, Notion, etc.

#### Module 5b : Data Store (Route 2)
- Sauvegarder les prompts générés pour historique
- Structure :
  - ID unique
  - Texte brut d'entrée
  - Prompt généré
  - JSON structuré
  - Timestamp

### Blueprint Make.com (importable)

```json
{
  "name": "Générateur de Prompts No Code",
  "flow": [
    {
      "id": 1,
      "module": "gateway:CustomWebHook",
      "parameters": {
        "hook": "prompt-generator-webhook",
        "dataStructure": {
          "raw_text": "text"
        }
      }
    },
    {
      "id": 2,
      "module": "http:ActionSendData",
      "mapper": {
        "url": "https://your-api.com/generate",
        "method": "POST",
        "headers": [
          {
            "name": "Content-Type",
            "value": "application/json"
          }
        ],
        "qs": [],
        "bodyType": "raw",
        "parseResponse": true,
        "rawBody": "{\"raw_text\": \"{{1.raw_text}}\"}"
      }
    },
    {
      "id": 3,
      "module": "builtin:BasicRouter",
      "routes": [
        {
          "flow": [
            {
              "id": 4,
              "module": "google-sheets:ActionAddRow"
            }
          ]
        },
        {
          "flow": [
            {
              "id": 5,
              "module": "slack:sendMessage"
            }
          ]
        }
      ]
    }
  ]
}
```

---

## ⚡ n8n

### Workflow Structure

```
Webhook → Function (Python Executor) → Set Node → Switch → [Multiple Outputs]
```

### Configuration n8n

#### Node 1 : Webhook
```javascript
{
  "httpMethod": "POST",
  "path": "prompt-generator",
  "responseMode": "lastNode",
  "responseData": "allEntries"
}
```

#### Node 2 : Function Node (Exécution Python)

**Option A : Appel API externe**
```javascript
const axios = require('axios');

const inputText = $json.raw_text;

const response = await axios.post('https://your-api.com/generate', {
  raw_text: inputText
});

return {
  text_prompt: response.data.text_prompt,
  json_prompt: response.data.json_prompt
};
```

**Option B : Exécution locale (via Execute Command)**
```javascript
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

const inputText = $json.raw_text.replace(/"/g, '\\"');

const { stdout } = await execPromise(
  `python3 /path/to/prompt_generator.py "${inputText}"`
);

const result = JSON.parse(stdout);

return {
  text_prompt: result.text_prompt,
  json_prompt: result.json_prompt
};
```

#### Node 3 : Set Node (Formatage)
```javascript
{
  "values": {
    "prompt_text": "={{$json.text_prompt}}",
    "prompt_json": "={{$json.json_prompt}}",
    "timestamp": "={{$now}}",
    "input": "={{$json.raw_text}}"
  }
}
```

#### Node 4 : Switch (Routing conditionnel)
```javascript
{
  "mode": "rules",
  "rules": [
    {
      "rule": "={{$json.complexity > 3}}",
      "output": 0  // Route complexe
    },
    {
      "rule": "={{$json.complexity <= 3}}",
      "output": 1  // Route simple
    }
  ]
}
```

#### Nodes de sortie (exemples)

**Airtable Storage**
```javascript
{
  "operation": "create",
  "table": "Generated Prompts",
  "fields": {
    "Input Text": "={{$json.input}}",
    "Text Prompt": "={{$json.prompt_text}}",
    "JSON Prompt": "={{$json.prompt_json}}",
    "Created": "={{$json.timestamp}}"
  }
}
```

**Slack Notification**
```javascript
{
  "channel": "#automation-alerts",
  "text": "Nouveau prompt généré !",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Prompt généré avec succès*\n\n{{$json.prompt_text}}"
      }
    }
  ]
}
```

### Workflow n8n (JSON exportable)

```json
{
  "name": "Prompt Generator NoCode",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "parameters": {
        "httpMethod": "POST",
        "path": "prompt-gen",
        "responseMode": "lastNode"
      }
    },
    {
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300],
      "parameters": {
        "url": "=https://your-api.com/generate",
        "method": "POST",
        "jsonParameters": true,
        "options": {},
        "bodyParametersJson": "={\"raw_text\": \"{{$json['body']['raw_text']}}\"}"
      }
    },
    {
      "name": "Airtable",
      "type": "n8n-nodes-base.airtable",
      "position": [650, 300],
      "parameters": {
        "operation": "create",
        "application": "appXXXXXXXXXXXXXX",
        "table": "Prompts",
        "fields": {
          "mappingMode": "defineBelow",
          "value": {
            "Text": "={{$json['text_prompt']}}",
            "JSON": "={{$json['json_prompt']}}"
          }
        }
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{"node": "HTTP Request", "type": "main", "index": 0}]]
    },
    "HTTP Request": {
      "main": [[{"node": "Airtable", "type": "main", "index": 0}]]
    }
  }
}
```

---

## 🫧 Bubble.io

### Architecture de l'application

#### 1. Structure de la base de données

**Table : PromptRequests**
- `raw_text` (text)
- `text_prompt` (text, long text)
- `json_prompt` (text, long text)
- `created_date` (date)
- `user` (User)

**Table : PromptTemplates**
- `name` (text)
- `category` (text)
- `template` (text)

#### 2. API Connector Setup

**API Name:** PromptGenerator

**Call: GeneratePrompt**
- Type: **POST**
- Use as: Action
- Data type: JSON

**Endpoint:**
```
https://your-api.com/generate
```

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "raw_text": "<raw_text>"
}
```

**Parameters:**
- `raw_text` : text, Dynamic

**Response Structure:**
```json
{
  "text_prompt": "text",
  "json_prompt": "text"
}
```

#### 3. Interface utilisateur (Page Design)

**Composants:**

1. **Input TextArea**
   - Placeholder: "Décrivez votre besoin d'automatisation..."
   - Type: Multi-line
   - Height: 150px

2. **Button "Générer le Prompt"**
   - Background: Primary color
   - Workflow: Generate Prompt

3. **Group "Résultats"**
   - Visible when: PromptRequest is not empty

   **3a. Text Block "Prompt Optimisé"**
   - Content: `Result of Step 1 (Generate Prompt)'s text_prompt`
   - Format: Markdown

   **3b. Text Block "JSON Structuré"**
   - Content: `Result of Step 1 (Generate Prompt)'s json_prompt`
   - Font: Monospace
   - Background: Light gray

4. **Button "Copier le Prompt"**
   - Workflow: Copy to clipboard

5. **Button "Sauvegarder"**
   - Workflow: Save to database

#### 4. Workflows

**Workflow 1: Generate Prompt**

Trigger: Button "Générer le Prompt" is clicked

Steps:
1. **API Call - PromptGenerator - GeneratePrompt**
   - raw_text = `Input TextArea's value`

2. **Display Data in Group "Résultats"**
   - Set state: show results
   - Scroll to: Results group

**Workflow 2: Copy to Clipboard**

Trigger: Button "Copier" is clicked

Steps:
1. **Copy to clipboard**
   - Value: `Result of Step 1's text_prompt`

2. **Show Alert**
   - Message: "Prompt copié dans le presse-papier !"
   - Style: Success

**Workflow 3: Save Prompt**

Trigger: Button "Sauvegarder" is clicked

Steps:
1. **Create a new PromptRequest**
   - raw_text = `Input TextArea's value`
   - text_prompt = `Result of Generate Prompt's text_prompt`
   - json_prompt = `Result of Generate Prompt's json_prompt`
   - user = `Current User`

2. **Navigate to** Page "My Prompts"

#### 5. Backend Workflows (API Workflow)

**Endpoint: /api/1.1/wf/generate-prompt**

**Type:** POST

**Parameters:**
- `raw_text` (text, required)

**Actions:**
1. API Call to Python Backend
2. Return data as JSON

---

## 🐍 Backend Python (FastAPI)

Pour héberger le générateur comme API REST :

```python
# api_server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prompt_generator import generate_from_text

app = FastAPI(title="Prompt Generator API")

# CORS pour permettre les appels depuis Make, n8n, Bubble
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    raw_text: str

class PromptResponse(BaseModel):
    text_prompt: str
    json_prompt: str

@app.post("/generate", response_model=PromptResponse)
async def generate_prompt(request: PromptRequest):
    try:
        result = generate_from_text(request.raw_text)
        return PromptResponse(
            text_prompt=result["text_prompt"],
            json_prompt=result["json_prompt"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Déploiement:**
- **Railway:** `railway up`
- **Render:** Connecter repo GitHub
- **Heroku:** `heroku create && git push heroku main`
- **AWS Lambda:** Utiliser Mangum adapter
- **Google Cloud Run:** `gcloud run deploy`

---

## 🔐 Sécurité & Best Practices

### Authentification
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/generate")
async def generate_prompt(
    request: PromptRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Vérifier le token
    if credentials.credentials != "your-secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    # ...
```

### Rate Limiting (Make, n8n, Bubble)
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/generate")
@limiter.limit("10/minute")
async def generate_prompt(request: Request, data: PromptRequest):
    # ...
```

### Variables d'environnement
```bash
# .env
API_KEY=your-secret-key
ALLOWED_ORIGINS=https://your-bubble-app.com,https://make.com
MAX_TEXT_LENGTH=5000
```

---

## 📊 Monitoring & Analytics

### Logs structurés
```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/generate")
async def generate_prompt(request: PromptRequest):
    start_time = datetime.now()

    logger.info(f"Request received: {request.raw_text[:50]}...")

    result = generate_from_text(request.raw_text)

    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"Request completed in {duration}s")

    return result
```

### Métriques (pour Make/n8n dashboards)
- Nombre de prompts générés
- Temps moyen de génération
- Outils No Code les plus utilisés
- Taux d'erreur

---

## 🧪 Tests pour intégrations No Code

```python
# test_api.py
import requests

BASE_URL = "http://localhost:8000"

def test_make_integration():
    """Test pour Make.com"""
    payload = {
        "raw_text": "Connecter Airtable à Slack"
    }
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    assert response.status_code == 200
    assert "text_prompt" in response.json()
    print("✅ Make.com integration OK")

def test_n8n_integration():
    """Test pour n8n"""
    payload = {
        "raw_text": "Automatiser l'envoi d'emails depuis Google Sheets"
    }
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    data = response.json()
    assert "instructions" in data["json_prompt"]
    print("✅ n8n integration OK")

def test_bubble_integration():
    """Test pour Bubble"""
    payload = {
        "raw_text": "Créer un système de notification"
    }
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    assert response.headers["content-type"] == "application/json"
    print("✅ Bubble integration OK")

if __name__ == "__main__":
    test_make_integration()
    test_n8n_integration()
    test_bubble_integration()
    print("\n🎉 Toutes les intégrations fonctionnent !")
```

---

## 📚 Ressources supplémentaires

- [Documentation Make.com API](https://www.make.com/en/api-documentation)
- [n8n Custom Nodes](https://docs.n8n.io/integrations/creating-nodes/)
- [Bubble API Connector Guide](https://manual.bubble.io/core-resources/api/the-api-connector)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

✅ **Toutes les intégrations sont prêtes à être déployées en production!**
