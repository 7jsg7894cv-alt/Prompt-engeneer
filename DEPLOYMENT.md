# 🚀 Guide de Déploiement

Ce guide explique comment déployer Prompt Maître sur différentes plateformes cloud.

---

## ⚡ Déploiement rapide (Railway) - RECOMMANDÉ

**Railway** est la méthode la plus simple pour déployer l'application.

### Étapes :

1. **Créer un compte** sur [Railway.app](https://railway.app)

2. **Connecter votre repository GitHub**
   - Cliquer sur "New Project"
   - Sélectionner "Deploy from GitHub repo"
   - Autoriser Railway à accéder à vos repos
   - Sélectionner le repo `Prompt-engeneer`

3. **Configuration automatique**
   - Railway détecte automatiquement `railway.json` et `requirements.txt`
   - Le déploiement démarre immédiatement

4. **Obtenir l'URL**
   - Une fois déployé, Railway génère une URL type : `https://prompt-maitre-production.up.railway.app`
   - L'interface web sera accessible immédiatement

5. **Variables d'environnement (optionnel)**
   - Dans Settings → Variables, ajouter :
     - `PORT` : 8000 (auto-configuré par Railway)
     - `LOG_LEVEL` : INFO

### Temps de déploiement : ~2-3 minutes

---

## 🎨 Déploiement sur Render

Render offre un plan gratuit avec déploiement automatisé.

### Étapes :

1. **Créer un compte** sur [Render.com](https://render.com)

2. **Créer un nouveau Web Service**
   - Dashboard → New → Web Service
   - Connecter votre repository GitHub
   - Sélectionner `Prompt-engeneer`

3. **Configuration**
   - Name: `prompt-maitre`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`

4. **Déployer**
   - Cliquer sur "Create Web Service"
   - Render détecte `render.yaml` pour configuration automatique

5. **URL générée** : `https://prompt-maitre.onrender.com`

### ⚠️ Note : Le plan gratuit de Render met l'app en veille après inactivité (redémarrage ~30s)

---

## 🐳 Déploiement Docker (Fly.io, Digital Ocean, AWS)

### Fly.io (Recommandé pour Docker)

1. **Installer Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login et créer l'app**
   ```bash
   fly auth login
   fly launch
   ```

3. **Configuration interactive**
   - App name: `prompt-maitre-[votre-nom]`
   - Region: Choisir la plus proche
   - Database: Non (pas nécessaire)

4. **Déployer**
   ```bash
   fly deploy
   ```

5. **URL** : `https://prompt-maitre-[votre-nom].fly.dev`

### Digital Ocean App Platform

1. Aller sur [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Créer une nouvelle app depuis GitHub
3. Sélectionner le repo
4. Configuration :
   - Type: Web Service
   - Dockerfile: Sélectionner le Dockerfile existant
   - Port: 8000
   - Health Check: `/health`
5. Déployer

---

## ☁️ Déploiement sur services cloud traditionnels

### AWS Elastic Beanstalk

```bash
# Installer EB CLI
pip install awsebcli

# Initialiser
eb init -p python-3.9 prompt-maitre

# Créer environnement
eb create prompt-maitre-env

# Déployer
eb deploy

# Ouvrir l'app
eb open
```

### Google Cloud Run

```bash
# Build Docker image
gcloud builds submit --tag gcr.io/[PROJECT-ID]/prompt-maitre

# Deploy
gcloud run deploy prompt-maitre \
  --image gcr.io/[PROJECT-ID]/prompt-maitre \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure App Service

```bash
# Login
az login

# Créer resource group
az group create --name PromptMaitreRG --location eastus

# Créer App Service plan
az appservice plan create --name PromptMaitrePlan --resource-group PromptMaitreRG --sku B1 --is-linux

# Créer web app
az webapp create --resource-group PromptMaitreRG --plan PromptMaitrePlan --name prompt-maitre-[unique] --runtime "PYTHON|3.9"

# Déployer depuis GitHub
az webapp deployment source config --name prompt-maitre-[unique] --resource-group PromptMaitreRG --repo-url [GITHUB_URL] --branch main
```

---

## 🔧 Configuration post-déploiement

### Variables d'environnement recommandées

```bash
PORT=8000
LOG_LEVEL=INFO
ALLOWED_ORIGINS=*  # ou votre domaine spécifique
MAX_INPUT_LENGTH=5000
```

### Health Check

Toutes les plateformes peuvent utiliser : `/health`

### Performance

- **RAM minimale** : 512 MB
- **RAM recommandée** : 1 GB
- **CPU** : 1 vCPU suffit
- **Stockage** : 1 GB

---

## 🌐 Domaine personnalisé

### Railway
1. Settings → Networking → Custom Domain
2. Ajouter votre domaine
3. Configurer DNS (CNAME vers Railway)

### Render
1. Settings → Custom Domain
2. Ajouter domaine
3. Configurer DNS selon instructions

### Fly.io
```bash
fly certs add votre-domaine.com
```

---

## 📊 Monitoring

### Logs en temps réel

**Railway:**
```bash
railway logs
```

**Render:**
Via dashboard → Logs

**Fly.io:**
```bash
fly logs
```

### Métriques

Toutes les plateformes fournissent :
- CPU usage
- Memory usage
- Request count
- Response times

---

## 🔒 Sécurité

### HTTPS
✅ Automatique sur toutes les plateformes

### Rate Limiting
Pour ajouter rate limiting, décommenter dans `api_server.py` :

```python
from slowapi import Limiter
# ...
@limiter.limit("60/minute")
```

### Variables sensibles
Ne jamais commiter `.env` dans Git. Utiliser les variables d'environnement de la plateforme.

---

## 💰 Coûts estimés

| Plateforme | Plan gratuit | Plan payant |
|------------|--------------|-------------|
| Railway | $5 crédit/mois | $5-10/mois |
| Render | Gratuit (avec limitations) | $7/mois |
| Fly.io | Gratuit (3 apps) | $1.94-5/mois |
| Heroku | - | $7/mois |
| Vercel | Gratuit (limité) | $20/mois |

**Recommandation** : Railway pour production, Render pour démo/test

---

## 🆘 Dépannage

### L'app ne démarre pas
1. Vérifier les logs
2. S'assurer que `requirements.txt` est présent
3. Vérifier que le port est configuré via `$PORT`

### Erreur 502/503
- L'app met du temps à démarrer (normal sur plan gratuit)
- Attendre 30-60 secondes

### Static files non trouvés
- Vérifier que le dossier `static/` est bien inclus dans le déploiement
- Railway/Render copient automatiquement tous les fichiers

---

## ✅ Checklist de déploiement

- [ ] Repository Git configuré
- [ ] `requirements.txt` à jour
- [ ] Variables d'environnement configurées
- [ ] Health check fonctionne localement
- [ ] Tests passent
- [ ] Déploiement effectué
- [ ] URL de production fonctionnelle
- [ ] Interface web accessible
- [ ] API `/generate` testée
- [ ] Documentation `/docs` accessible

---

## 🎉 Félicitations !

Votre générateur de prompts est maintenant déployé et accessible publiquement !

**Prochaines étapes** :
1. Partager l'URL avec vos utilisateurs
2. Configurer un domaine personnalisé (optionnel)
3. Ajouter des analytics (optionnel)
4. Monitorer les performances

---

**Support** : Pour toute question, ouvrir une issue sur GitHub
