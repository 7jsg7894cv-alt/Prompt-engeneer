# 🚀 Guide de Démarrage Rapide

Commencez à utiliser le Générateur de Prompts No Code en 5 minutes !

---

## 📦 Option 1 : Utilisation locale (Python)

### Prérequis
- Python 3.8 ou supérieur
- pip

### Installation

```bash
# 1. Cloner le repository
git clone https://github.com/votre-repo/prompt-maitre.git
cd prompt-maitre

# 2. Installer les dépendances
pip install -r requirements.txt
```

### Test rapide

```bash
# Tester le générateur en mode CLI
python prompt_generator.py
```

**Résultat** : Vous verrez un exemple de génération complet

### Exécuter les exemples

```bash
# Voir 5 exemples différents
python examples.py
```

---

## 🌐 Option 2 : Lancer l'API REST

### Démarrage simple

```bash
# Lancer le serveur FastAPI
python api_server.py
```

L'API sera accessible sur :
- **API** : http://localhost:8000
- **Documentation** : http://localhost:8000/docs
- **Redoc** : http://localhost:8000/redoc

### Tester l'API

**Avec curl :**
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"raw_text": "Je veux connecter Airtable à Slack"}'
```

**Avec httpie :**
```bash
http POST localhost:8000/generate raw_text="Connecter Airtable à Slack"
```

**Avec Python requests :**
```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={"raw_text": "Je veux connecter Airtable à Slack"}
)

result = response.json()
print(result["text_prompt"])
```

---

## 🐳 Option 3 : Docker

### Démarrage avec Docker

```bash
# Construire l'image
docker build -t prompt-maitre .

# Lancer le conteneur
docker run -p 8000:8000 prompt-maitre
```

### Démarrage avec Docker Compose

```bash
# Lancer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f prompt-api

# Arrêter
docker-compose down
```

---

## 🔌 Option 4 : Intégration No Code

### Make.com

1. Créer un nouveau scénario
2. Ajouter un webhook comme déclencheur
3. Ajouter un module **HTTP Request** :
   - URL : `http://localhost:8000/generate` (ou votre URL de production)
   - Method : POST
   - Body :
     ```json
     {
       "raw_text": "{{1.raw_text}}"
     }
     ```
4. Parser la réponse JSON
5. Utiliser `text_prompt` ou `json_prompt`

### n8n

1. Créer un nouveau workflow
2. Ajouter un node **Webhook**
3. Ajouter un node **HTTP Request** :
   - Method : POST
   - URL : `http://localhost:8000/generate`
   - Body :
     ```json
     {
       "raw_text": "={{$json.body.raw_text}}"
     }
     ```
4. Ajouter un node **Set** pour formater la sortie

### Bubble.io

1. Ouvrir **Plugins** → **API Connector**
2. Créer une nouvelle API : "PromptGenerator"
3. Ajouter un call :
   - Name : GeneratePrompt
   - Use as : Action
   - Data type : JSON
   - Method : POST
   - URL : `http://votre-api.com/generate`
   - Body :
     ```json
     {
       "raw_text": "<raw_text>"
     }
     ```
4. Initialiser et utiliser dans vos workflows

---

## 🧪 Option 5 : Exécuter les tests

```bash
# Installer pytest
pip install pytest pytest-asyncio httpx

# Exécuter tous les tests
pytest test_api.py -v

# Exécuter un test spécifique
pytest test_api.py::TestAPI::test_generate_endpoint_success -v

# Avec coverage
pytest test_api.py --cov=prompt_generator --cov=api_server
```

---

## 📊 Exemples d'utilisation

### Exemple 1 : Connexion simple

**Entrée :**
```
"Je veux connecter Airtable à Slack pour être notifié"
```

**Sortie :** Prompt complet avec :
- Rôle d'expert
- Instructions étape par étape
- Configuration recommandée

### Exemple 2 : Workflow avec IA

**Entrée :**
```
"Utiliser OpenAI pour analyser les feedbacks clients depuis Notion"
```

**Sortie :** Prompt avancé incluant :
- Intégration IA
- Gestion des erreurs
- Contraintes d'API

### Exemple 3 : Synchronisation complexe

**Entrée :**
```
"Synchroniser bidirectionnellement Notion et Airtable avec transformation des données"
```

**Sortie :** Architecture complète avec :
- Flux bidirectionnel
- Transformation de données
- Gestion des conflits

---

## 🔧 Configuration avancée

### Variables d'environnement

```bash
# Copier le template
cp .env.example .env

# Éditer les variables
nano .env
```

**Variables importantes :**
- `PORT` : Port du serveur (défaut : 8000)
- `LOG_LEVEL` : Niveau de log (INFO, DEBUG, ERROR)
- `ALLOWED_ORIGINS` : Domaines autorisés pour CORS
- `MAX_INPUT_LENGTH` : Longueur max du texte (défaut : 5000)

---

## 📖 Commandes utiles

```bash
# Voir l'état de l'API
curl http://localhost:8000/health

# Lister les outils supportés
curl http://localhost:8000/tools

# Voir les intentions détectables
curl http://localhost:8000/intents

# Obtenir le schéma JSON
curl http://localhost:8000/schema

# Voir des exemples
curl http://localhost:8000/examples
```

---

## 🐛 Résolution de problèmes

### L'API ne démarre pas

```bash
# Vérifier que le port 8000 n'est pas déjà utilisé
lsof -i :8000

# Utiliser un autre port
PORT=8080 python api_server.py
```

### Erreur d'import

```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Tests échouent

```bash
# Installer les dépendances de test
pip install pytest pytest-asyncio httpx

# Lancer avec plus de détails
pytest test_api.py -v --tb=long
```

---

## 📚 Prochaines étapes

1. **Explorer la documentation complète** : Voir [README.md](./README.md)
2. **Intégrer dans votre workflow** : Voir [nocode_integrations.md](./nocode_integrations.md)
3. **Déployer en production** : Voir les options de déploiement
4. **Contribuer** : Voir [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 💬 Support

- **Documentation** : [README.md](./README.md)
- **Issues** : https://github.com/votre-repo/issues
- **Discussions** : https://github.com/votre-repo/discussions

---

✅ **Vous êtes prêt à générer vos premiers prompts optimisés !**
