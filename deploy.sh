#!/bin/bash

echo "================================="
echo "🚀 DÉPLOIEMENT AUTOMATIQUE"
echo "Prompt Maître sur Railway"
echo "================================="
echo ""

# Vérifier si Railway CLI est installé
if ! command -v railway &> /dev/null; then
    echo "📦 Installation de Railway CLI..."

    # Détecter l'OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://railway.app/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install railway
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        echo "⚠️  Sur Windows, téléchargez Railway CLI depuis:"
        echo "https://docs.railway.app/develop/cli#windows"
        exit 1
    fi
else
    echo "✅ Railway CLI déjà installé"
fi

echo ""
echo "🔐 Connexion à Railway..."
echo "Une fenêtre de navigateur va s'ouvrir pour l'authentification"
railway login

echo ""
echo "📋 Initialisation du projet..."
railway init

echo ""
echo "🚀 Déploiement en cours..."
railway up

echo ""
echo "================================="
echo "✅ DÉPLOIEMENT TERMINÉ !"
echo "================================="
echo ""
echo "🌐 Votre application est en ligne !"
echo ""
echo "Pour obtenir l'URL publique:"
echo "  railway domain"
echo ""
echo "Pour voir les logs:"
echo "  railway logs"
echo ""
echo "Pour ouvrir l'app dans le navigateur:"
echo "  railway open"
echo ""
