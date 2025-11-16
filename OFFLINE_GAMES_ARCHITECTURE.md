# 🎮 Architecture Fullstack - Page de Jeux Offline avec Shadcn UI

## 📋 Vue d'ensemble du projet

Une plateforme de jeux web jouables sans connexion, inspirée de Jeu.fr, avec une interface moderne utilisant Shadcn UI et React/Next.js.

---

## 🏗️ Architecture Technique

### Stack Technologique

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND                               │
├─────────────────────────────────────────────────────────────┤
│  Framework        : Next.js 14 (App Router)                 │
│  UI Library       : React 18                                │
│  UI Components    : Shadcn/UI                               │
│  Styling          : Tailwind CSS                            │
│  State Management : Zustand / React Context                 │
│  Animations       : Framer Motion                           │
│  Icons            : Lucide React                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      OFFLINE SUPPORT                        │
├─────────────────────────────────────────────────────────────┤
│  PWA              : Next-PWA                                │
│  Service Worker   : Workbox                                 │
│  Cache Strategy   : Cache First + Network Fallback         │
│  Storage          : LocalStorage + IndexedDB                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      BUILD & DEPLOY                         │
├─────────────────────────────────────────────────────────────┤
│  Package Manager  : pnpm                                    │
│  Linter           : ESLint                                  │
│  Formatter        : Prettier                                │
│  Type Checking    : TypeScript                              │
│  Deployment       : Vercel / Netlify                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Jeux à Développer (Phase 1)

### 1. 🐍 Snake Game
**Complexité**: ⭐⭐ (Simple)
- Grille de jeu 20x20
- Contrôles: clavier (flèches) + tactile (swipe)
- Score + high score (LocalStorage)
- Vitesse progressive
- Animations fluides

### 2. ⭕ Tic-Tac-Toe
**Complexité**: ⭐ (Très simple)
- Mode: Joueur vs IA (algorithme Minimax)
- Interface drag & drop optionnelle
- Historique des coups
- Animation de victoire

### 3. 🃏 Memory Card Game
**Complexité**: ⭐⭐ (Simple)
- Grille 4x4 (8 paires)
- Thèmes multiples (emojis, icons)
- Timer + nombre de coups
- Niveaux de difficulté (4x4, 6x6, 8x8)

### 4. 🔢 2048
**Complexité**: ⭐⭐⭐ (Intermédiaire)
- Grille 4x4
- Swipe gestures
- Animation de fusion
- Undo feature
- Best score tracking

### 5. 🧩 Tetris (Phase 2)
**Complexité**: ⭐⭐⭐⭐ (Avancé)
- Grille 10x20
- 7 types de pièces
- Rotation + hard drop
- Score + lignes + niveau

---

## 📂 Structure du Projet

```
games-platform/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Layout principal
│   ├── page.tsx                 # Page d'accueil (liste des jeux)
│   ├── games/
│   │   ├── snake/
│   │   │   ├── page.tsx         # Page du jeu Snake
│   │   │   └── components/      # Composants spécifiques
│   │   ├── tic-tac-toe/
│   │   │   └── page.tsx
│   │   ├── memory/
│   │   │   └── page.tsx
│   │   └── 2048/
│   │       └── page.tsx
│   └── api/                     # API routes (optionnel)
│       └── scores/
│           └── route.ts
│
├── components/                   # Composants réutilisables
│   ├── ui/                      # Shadcn UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── badge.tsx
│   │   └── ...
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Navigation.tsx
│   ├── games/
│   │   ├── GameCard.tsx         # Carte pour afficher un jeu
│   │   ├── GameLayout.tsx       # Layout commun pour tous les jeux
│   │   ├── ScoreBoard.tsx       # Tableau des scores
│   │   └── GameControls.tsx     # Contrôles communs
│   └── common/
│       ├── LoadingSpinner.tsx
│       └── ErrorBoundary.tsx
│
├── lib/                         # Logique métier
│   ├── games/
│   │   ├── snake/
│   │   │   ├── engine.ts        # Moteur de jeu
│   │   │   ├── types.ts         # Types TypeScript
│   │   │   └── constants.ts     # Constantes
│   │   ├── tic-tac-toe/
│   │   │   ├── ai.ts            # IA Minimax
│   │   │   └── game-logic.ts
│   │   ├── memory/
│   │   │   └── card-generator.ts
│   │   └── 2048/
│   │       └── game-engine.ts
│   ├── storage/
│   │   ├── local-storage.ts     # Wrapper LocalStorage
│   │   └── indexed-db.ts        # Wrapper IndexedDB
│   ├── hooks/
│   │   ├── useGameState.ts      # Hook state de jeu
│   │   ├── useLocalStorage.ts   # Hook storage
│   │   └── useOfflineStatus.ts  # Détection offline
│   └── utils/
│       ├── score-manager.ts     # Gestion des scores
│       └── analytics.ts         # Analytics (optionnel)
│
├── stores/                      # State management (Zustand)
│   ├── game-store.ts
│   └── user-store.ts
│
├── styles/
│   └── globals.css              # Styles globaux + Tailwind
│
├── public/
│   ├── icons/                   # Icônes de jeux
│   ├── images/
│   ├── manifest.json            # PWA Manifest
│   └── sw.js                    # Service Worker
│
├── types/
│   └── games.ts                 # Types globaux
│
├── next.config.js               # Configuration Next.js
├── tailwind.config.js           # Configuration Tailwind
├── tsconfig.json                # Configuration TypeScript
├── package.json
└── .env.local                   # Variables d'environnement

```

---

## 🎨 Design System (Shadcn UI)

### Palette de Couleurs

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;

  --primary: 262 83% 58%;        /* Violet pour thème gaming */
  --primary-foreground: 210 40% 98%;

  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;

  --accent: 142 71% 45%;         /* Vert pour succès */
  --accent-foreground: 222.2 47.4% 11.2%;

  --destructive: 0 84.2% 60.2%;  /* Rouge pour game over */
  --destructive-foreground: 210 40% 98%;

  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;

  --primary: 262 83% 58%;
  --primary-foreground: 210 40% 98%;

  /* ... mode sombre */
}
```

### Composants Shadcn à Installer

```bash
# Installation des composants nécessaires
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add separator
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add avatar
npx shadcn-ui@latest add progress
```

### Exemples d'UI

#### GameCard Component
```tsx
<Card className="group hover:shadow-xl transition-all duration-300">
  <CardHeader>
    <div className="flex items-center justify-between">
      <Badge variant="outline">{category}</Badge>
      <Badge variant="secondary">{difficulty}</Badge>
    </div>
  </CardHeader>
  <CardContent>
    <div className="relative overflow-hidden rounded-lg">
      <Image src={thumbnail} alt={name} />
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
    </div>
    <h3 className="text-xl font-bold mt-4">{name}</h3>
    <p className="text-muted-foreground">{description}</p>
  </CardContent>
  <CardFooter>
    <Button className="w-full">
      <PlayIcon className="mr-2" />
      Jouer
    </Button>
  </CardFooter>
</Card>
```

---

## 🔄 Flux de Développement

### Phase 1: Setup (Jour 1)
```bash
# 1. Initialiser Next.js
npx create-next-app@latest games-platform --typescript --tailwind --app

# 2. Installer Shadcn UI
npx shadcn-ui@latest init

# 3. Installer les dépendances
pnpm add zustand framer-motion lucide-react
pnpm add -D @types/node

# 4. Installer PWA support
pnpm add next-pwa
```

### Phase 2: UI Foundation (Jour 2-3)
- Créer le layout principal
- Installer les composants Shadcn
- Créer les composants de base (Header, Navigation, Footer)
- Implémenter le theme switcher (dark/light)
- Créer la page d'accueil avec la grille de jeux

### Phase 3: Développement des Jeux (Jour 4-10)

#### Snake (Jour 4-5)
1. Créer le canvas/grille
2. Implémenter la logique de mouvement
3. Gérer les collisions
4. Système de score
5. Animations

#### Tic-Tac-Toe (Jour 6)
1. Grille 3x3
2. Logique de victoire
3. IA Minimax
4. UI/UX

#### Memory (Jour 7-8)
1. Générateur de cartes
2. Logique de match
3. Timer
4. Niveaux

#### 2048 (Jour 9-10)
1. Grille 4x4
2. Logique de fusion
3. Swipe gestures
4. Animations

### Phase 4: PWA & Offline (Jour 11-12)
- Configurer Service Worker
- Implémenter cache strategies
- Tester offline
- Optimiser les assets
- Créer le manifest.json

### Phase 5: Polish & Deploy (Jour 13-14)
- Tests cross-browser
- Performance optimization
- SEO
- Déploiement Vercel
- Documentation

---

## 💾 Gestion des Données Offline

### LocalStorage Structure

```typescript
interface GameStorage {
  snake: {
    highScore: number;
    gamesPlayed: number;
    lastPlayed: string;
  };
  ticTacToe: {
    wins: number;
    losses: number;
    draws: number;
  };
  memory: {
    bestTime: Record<string, number>; // par niveau
    completedLevels: string[];
  };
  game2048: {
    highScore: number;
    currentGame?: GameState;
  };
  settings: {
    theme: 'light' | 'dark';
    soundEnabled: boolean;
    difficulty: 'easy' | 'medium' | 'hard';
  };
}
```

### Service Worker Cache Strategy

```javascript
// next.config.js avec next-pwa
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

module.exports = withPWA({
  // Next.js config
});
```

---

## 🎮 API des Jeux

### Interface Commune pour tous les jeux

```typescript
interface Game {
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
  estimatedDuration: number; // en minutes
}

interface GameState {
  isPlaying: boolean;
  isPaused: boolean;
  isGameOver: boolean;
  score: number;
  startTime?: Date;
  endTime?: Date;
}

interface GameActions {
  start: () => void;
  pause: () => void;
  resume: () => void;
  restart: () => void;
  quit: () => void;
}
```

---

## 🚀 Commandes de Développement

```bash
# Développement
pnpm dev              # Lancer le serveur de dev (localhost:3000)

# Build
pnpm build            # Build production
pnpm start            # Lancer le build en production

# Tests
pnpm lint             # ESLint
pnpm type-check       # TypeScript check

# Shadcn
npx shadcn-ui@latest add [component]  # Ajouter un composant

# PWA
pnpm build && pnpm start  # Tester le PWA en local
```

---

## 📊 Métriques de Performance

### Objectifs
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **Lighthouse Score**: > 90
- **Bundle Size**: < 200kb (initial)
- **Offline Ready**: 100%

### Optimisations
- Code splitting par route
- Image optimization (next/image)
- Font optimization
- CSS purging (Tailwind)
- Service Worker caching

---

## 🔐 Sécurité & Best Practices

1. **Content Security Policy**: Headers strictes
2. **No External Dependencies** pour les jeux (tout en local)
3. **LocalStorage Encryption**: Pour les données sensibles
4. **Input Validation**: Pour tous les scores/inputs
5. **Rate Limiting**: Pour les API routes (si utilisées)

---

## 📱 Responsive Design

```css
/* Breakpoints Tailwind */
sm: 640px   /* Mobile landscape */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
2xl: 1536px /* Extra large */
```

### Adaptations
- **Mobile**: Grille 1 colonne, contrôles tactiles
- **Tablet**: Grille 2 colonnes
- **Desktop**: Grille 3-4 colonnes, contrôles clavier

---

## 🎯 Roadmap

### Version 1.0 (MVP)
- [x] Setup projet Next.js + Shadcn
- [ ] 4 jeux fonctionnels
- [ ] Mode offline complet
- [ ] Responsive design
- [ ] Déploiement

### Version 1.1
- [ ] Ajout de Tetris
- [ ] Système de succès/achievements
- [ ] Leaderboard local
- [ ] Partage de scores (image)

### Version 2.0
- [ ] Multijoueur local (même appareil)
- [ ] Plus de jeux (Sudoku, Chess, etc.)
- [ ] Thèmes personnalisables
- [ ] Export/Import de données

---

## 📚 Ressources

### Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [Shadcn UI](https://ui.shadcn.com)
- [Tailwind CSS](https://tailwindcss.com)
- [PWA Guide](https://web.dev/progressive-web-apps/)

### Inspiration Design
- [Jeu.fr](https://www.jeu.fr)
- [Poki](https://poki.com)
- [CrazyGames](https://www.crazygames.com)

---

## 🤝 Contribution

Ce projet est open source. Les contributions sont bienvenues!

### Ajouter un nouveau jeu

1. Créer le dossier `app/games/[game-name]/`
2. Implémenter la logique dans `lib/games/[game-name]/`
3. Ajouter les types dans `types/games.ts`
4. Créer les composants UI
5. Enregistrer le jeu dans la config

---

**Auteur**: Claude
**License**: MIT
**Version**: 1.0.0
**Date**: 2025-11-16
