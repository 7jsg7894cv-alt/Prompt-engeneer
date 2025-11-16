#!/bin/bash

# 🎮 Script d'installation automatique de la plateforme de jeux offline
# Avec Next.js 14, Shadcn UI et PWA support

set -e  # Arrêter en cas d'erreur

echo "🎮 =========================================="
echo "   Setup Plateforme de Jeux Offline"
echo "   Next.js + Shadcn UI + PWA"
echo "=========================================="
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
PROJECT_NAME="games-platform"
PROJECT_DIR="$PROJECT_NAME"

# Vérifier si pnpm est installé
if ! command -v pnpm &> /dev/null; then
    echo -e "${YELLOW}⚠️  pnpm n'est pas installé. Installation...${NC}"
    npm install -g pnpm
fi

echo -e "${BLUE}📦 Étape 1/7: Création du projet Next.js...${NC}"
npx create-next-app@latest $PROJECT_NAME \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir \
  --import-alias "@/*" \
  --use-pnpm

cd $PROJECT_DIR

echo ""
echo -e "${GREEN}✅ Projet Next.js créé${NC}"
echo ""

echo -e "${BLUE}🎨 Étape 2/7: Installation de Shadcn UI...${NC}"
# Initialiser Shadcn UI (répondre automatiquement aux prompts)
npx shadcn-ui@latest init -d

echo ""
echo -e "${GREEN}✅ Shadcn UI initialisé${NC}"
echo ""

echo -e "${BLUE}🧩 Étape 3/7: Installation des composants Shadcn...${NC}"
# Installer les composants nécessaires
COMPONENTS=(
  "button"
  "card"
  "dialog"
  "badge"
  "separator"
  "toast"
  "dropdown-menu"
  "tabs"
  "avatar"
  "progress"
  "switch"
  "slider"
)

for component in "${COMPONENTS[@]}"; do
  echo "  → Installation de $component..."
  npx shadcn-ui@latest add $component -y
done

echo ""
echo -e "${GREEN}✅ Composants Shadcn installés${NC}"
echo ""

echo -e "${BLUE}📚 Étape 4/7: Installation des dépendances...${NC}"
pnpm add zustand framer-motion lucide-react class-variance-authority clsx tailwind-merge
pnpm add next-pwa
pnpm add -D @types/node

echo ""
echo -e "${GREEN}✅ Dépendances installées${NC}"
echo ""

echo -e "${BLUE}📁 Étape 5/7: Création de la structure des dossiers...${NC}"

# Créer la structure des dossiers
mkdir -p app/games/{snake,tic-tac-toe,memory,2048}/components
mkdir -p components/{ui,layout,games,common}
mkdir -p lib/{games/{snake,tic-tac-toe,memory,2048},storage,hooks,utils}
mkdir -p stores
mkdir -p types
mkdir -p public/{icons,images}

echo "  → Structure des dossiers créée"
echo ""
echo -e "${GREEN}✅ Structure créée${NC}"
echo ""

echo -e "${BLUE}⚙️  Étape 6/7: Configuration du PWA...${NC}"

# Créer next.config.js avec PWA
cat > next.config.js << 'EOF'
/** @type {import('next').NextConfig} */
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development',
  runtimeCaching: [
    {
      urlPattern: /^https?.*/,
      handler: 'CacheFirst',
      options: {
        cacheName: 'offlineCache',
        expiration: {
          maxEntries: 200,
          maxAgeSeconds: 30 * 24 * 60 * 60, // 30 jours
        },
      },
    },
  ],
});

const nextConfig = {
  // Configuration Next.js
};

module.exports = withPWA(nextConfig);
EOF

# Créer manifest.json
cat > public/manifest.json << 'EOF'
{
  "name": "Plateforme de Jeux Offline",
  "short_name": "Games",
  "description": "Collection de jeux web jouables sans connexion",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#8B5CF6",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
EOF

echo "  → Configuration PWA créée"
echo ""
echo -e "${GREEN}✅ PWA configuré${NC}"
echo ""

echo -e "${BLUE}📝 Étape 7/7: Création des fichiers de base...${NC}"

# Créer types/games.ts
cat > types/games.ts << 'EOF'
export interface Game {
  id: string;
  name: string;
  slug: string;
  description: string;
  thumbnail: string;
  category: 'action' | 'puzzle' | 'strategy' | 'arcade';
  difficulty: 'easy' | 'medium' | 'hard';
  minPlayers: number;
  maxPlayers: number;
  offlineSupport: boolean;
  estimatedDuration: number;
}

export interface GameState {
  isPlaying: boolean;
  isPaused: boolean;
  isGameOver: boolean;
  score: number;
  startTime?: Date;
  endTime?: Date;
}

export interface GameActions {
  start: () => void;
  pause: () => void;
  resume: () => void;
  restart: () => void;
  quit: () => void;
}
EOF

# Créer lib/utils/cn.ts (si pas déjà créé par Shadcn)
cat > lib/utils.ts << 'EOF'
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
EOF

# Créer le store Zustand
cat > stores/game-store.ts << 'EOF'
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface GameStats {
  gamesPlayed: number;
  totalScore: number;
  highScores: Record<string, number>;
}

interface GameStoreState {
  stats: GameStats;
  updateHighScore: (gameId: string, score: number) => void;
  incrementGamesPlayed: () => void;
}

export const useGameStore = create<GameStoreState>()(
  persist(
    (set) => ({
      stats: {
        gamesPlayed: 0,
        totalScore: 0,
        highScores: {},
      },
      updateHighScore: (gameId, score) =>
        set((state) => ({
          stats: {
            ...state.stats,
            highScores: {
              ...state.stats.highScores,
              [gameId]: Math.max(state.stats.highScores[gameId] || 0, score),
            },
          },
        })),
      incrementGamesPlayed: () =>
        set((state) => ({
          stats: {
            ...state.stats,
            gamesPlayed: state.stats.gamesPlayed + 1,
          },
        })),
    }),
    {
      name: 'game-storage',
    }
  )
);
EOF

# Créer un README pour le nouveau projet
cat > README_GAMES.md << 'EOF'
# 🎮 Plateforme de Jeux Offline

Une collection de jeux web jouables sans connexion, construite avec Next.js 14, Shadcn UI et PWA.

## 🚀 Démarrage Rapide

```bash
# Installer les dépendances (si pas déjà fait)
pnpm install

# Lancer le serveur de développement
pnpm dev

# Ouvrir http://localhost:3000
```

## 🎯 Jeux Disponibles

- 🐍 Snake
- ⭕ Tic-Tac-Toe
- 🃏 Memory Card
- 🔢 2048

## 📦 Stack Technique

- **Framework**: Next.js 14 (App Router)
- **UI**: Shadcn/UI + Tailwind CSS
- **State**: Zustand
- **Animations**: Framer Motion
- **Offline**: PWA + Service Worker

## 📖 Documentation

Voir [OFFLINE_GAMES_ARCHITECTURE.md](../OFFLINE_GAMES_ARCHITECTURE.md) pour l'architecture complète.

## 🛠️ Commandes

```bash
pnpm dev          # Développement
pnpm build        # Build production
pnpm start        # Serveur production
pnpm lint         # Linter
```

## 📱 PWA

Le projet est configuré comme PWA. Pour tester:

```bash
pnpm build
pnpm start
# Ouvrir en mode navigation privée et installer l'app
```
EOF

echo "  → Fichiers de base créés"
echo ""
echo -e "${GREEN}✅ Configuration terminée${NC}"
echo ""

echo -e "${GREEN}🎉 =========================================="
echo "   Installation terminée avec succès!"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}📍 Prochaines étapes:${NC}"
echo ""
echo "  cd $PROJECT_NAME"
echo "  pnpm dev"
echo ""
echo -e "${BLUE}📖 Documentation: README_GAMES.md${NC}"
echo -e "${BLUE}🏗️  Architecture: ../OFFLINE_GAMES_ARCHITECTURE.md${NC}"
echo ""
echo -e "${GREEN}Bon développement! 🚀${NC}"
