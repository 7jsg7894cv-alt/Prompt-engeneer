# 🎮 Guide de Développement - Plateforme de Jeux Offline

## 📚 Table des matières

1. [Installation et Setup](#installation-et-setup)
2. [Développement des Jeux](#développement-des-jeux)
3. [Templates de Code](#templates-de-code)
4. [Best Practices](#best-practices)
5. [Testing et Debugging](#testing-et-debugging)
6. [Déploiement](#déploiement)

---

## 🚀 Installation et Setup

### Méthode 1: Script Automatique (Recommandé)

```bash
# Donner les permissions d'exécution
chmod +x setup-games-platform.sh

# Exécuter le script
./setup-games-platform.sh

# Attendre la fin de l'installation (5-10 minutes)
# Le script va:
#   1. Créer le projet Next.js
#   2. Installer Shadcn UI
#   3. Ajouter tous les composants nécessaires
#   4. Configurer le PWA
#   5. Créer la structure des dossiers
```

### Méthode 2: Installation Manuelle

```bash
# 1. Créer le projet
npx create-next-app@latest games-platform --typescript --tailwind --app --use-pnpm

cd games-platform

# 2. Initialiser Shadcn
npx shadcn-ui@latest init

# 3. Ajouter les composants
npx shadcn-ui@latest add button card dialog badge toast

# 4. Installer les dépendances
pnpm add zustand framer-motion lucide-react next-pwa
```

### Vérification de l'installation

```bash
cd games-platform
pnpm dev

# Ouvrir http://localhost:3000
# Vous devriez voir la page par défaut de Next.js
```

---

## 🎯 Développement des Jeux

### Phase 1: Page d'Accueil

#### 1. Créer le fichier `app/page.tsx`

```tsx
import { GameCard } from '@/components/games/GameCard';
import { games } from '@/lib/games-config';

export default function HomePage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-4">
          🎮 Jeux Offline
        </h1>
        <p className="text-xl text-muted-foreground">
          Jouez sans connexion à vos jeux préférés
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {games.map((game) => (
          <GameCard key={game.id} game={game} />
        ))}
      </div>
    </main>
  );
}
```

#### 2. Créer la configuration des jeux `lib/games-config.ts`

```typescript
import { Game } from '@/types/games';

export const games: Game[] = [
  {
    id: 'snake',
    name: 'Snake',
    slug: 'snake',
    description: 'Le classique Snake revisité. Mangez les pommes et grandissez!',
    thumbnail: '/images/snake.png',
    category: 'arcade',
    difficulty: 'easy',
    minPlayers: 1,
    maxPlayers: 1,
    offlineSupport: true,
    estimatedDuration: 5,
  },
  {
    id: 'tic-tac-toe',
    name: 'Tic-Tac-Toe',
    slug: 'tic-tac-toe',
    description: 'Affrontez l\'IA dans ce jeu de stratégie classique',
    thumbnail: '/images/tictactoe.png',
    category: 'strategy',
    difficulty: 'easy',
    minPlayers: 1,
    maxPlayers: 2,
    offlineSupport: true,
    estimatedDuration: 2,
  },
  {
    id: 'memory',
    name: 'Memory Card',
    slug: 'memory',
    description: 'Testez votre mémoire avec ce jeu de cartes amusant',
    thumbnail: '/images/memory.png',
    category: 'puzzle',
    difficulty: 'medium',
    minPlayers: 1,
    maxPlayers: 1,
    offlineSupport: true,
    estimatedDuration: 10,
  },
  {
    id: '2048',
    name: '2048',
    slug: '2048',
    description: 'Combinez les tuiles pour atteindre 2048!',
    thumbnail: '/images/2048.png',
    category: 'puzzle',
    difficulty: 'medium',
    minPlayers: 1,
    maxPlayers: 1,
    offlineSupport: true,
    estimatedDuration: 15,
  },
];
```

#### 3. Créer le composant `GameCard`

```tsx
// components/games/GameCard.tsx
'use client';

import { Game } from '@/types/games';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Play, Clock, Users } from 'lucide-react';
import Link from 'next/link';

interface GameCardProps {
  game: Game;
}

export function GameCard({ game }: GameCardProps) {
  const difficultyColor = {
    easy: 'bg-green-500',
    medium: 'bg-yellow-500',
    hard: 'bg-red-500',
  };

  return (
    <Card className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
      <CardHeader className="space-y-2">
        <div className="flex items-center justify-between">
          <Badge variant="outline" className="capitalize">
            {game.category}
          </Badge>
          <Badge
            variant="secondary"
            className={`${difficultyColor[game.difficulty]} text-white`}
          >
            {game.difficulty}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        <div className="aspect-video bg-gradient-to-br from-violet-500 to-purple-600 rounded-lg flex items-center justify-center text-6xl">
          {game.id === 'snake' && '🐍'}
          {game.id === 'tic-tac-toe' && '⭕'}
          {game.id === 'memory' && '🃏'}
          {game.id === '2048' && '🔢'}
        </div>

        <div>
          <h3 className="text-xl font-bold mb-2">{game.name}</h3>
          <p className="text-sm text-muted-foreground">
            {game.description}
          </p>
        </div>

        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-1">
            <Clock className="w-4 h-4" />
            <span>{game.estimatedDuration} min</span>
          </div>
          <div className="flex items-center gap-1">
            <Users className="w-4 h-4" />
            <span>{game.minPlayers}-{game.maxPlayers}</span>
          </div>
        </div>
      </CardContent>

      <CardFooter>
        <Link href={`/games/${game.slug}`} className="w-full">
          <Button className="w-full group-hover:bg-violet-600" size="lg">
            <Play className="w-4 h-4 mr-2" />
            Jouer
          </Button>
        </Link>
      </CardFooter>
    </Card>
  );
}
```

### Phase 2: Développer le Jeu Snake

#### 1. Structure du jeu

```
lib/games/snake/
├── engine.ts          # Logique du jeu
├── types.ts           # Types TypeScript
├── constants.ts       # Constantes (taille grille, vitesse, etc.)
└── utils.ts           # Fonctions utilitaires
```

#### 2. Créer les types `lib/games/snake/types.ts`

```typescript
export interface Position {
  x: number;
  y: number;
}

export type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT';

export interface SnakeGameState {
  snake: Position[];
  food: Position;
  direction: Direction;
  nextDirection: Direction;
  score: number;
  isGameOver: boolean;
  isPaused: boolean;
}

export const INITIAL_STATE: SnakeGameState = {
  snake: [
    { x: 10, y: 10 },
    { x: 10, y: 11 },
    { x: 10, y: 12 },
  ],
  food: { x: 15, y: 15 },
  direction: 'UP',
  nextDirection: 'UP',
  score: 0,
  isGameOver: false,
  isPaused: false,
};
```

#### 3. Créer les constantes `lib/games/snake/constants.ts`

```typescript
export const GRID_SIZE = 20;
export const CELL_SIZE = 25;
export const INITIAL_SPEED = 150; // ms
export const SPEED_INCREMENT = 10; // Accélération tous les 5 points

export const COLORS = {
  snake: '#8B5CF6',
  food: '#10B981',
  background: '#1F2937',
  grid: '#374151',
};
```

#### 4. Créer le moteur de jeu `lib/games/snake/engine.ts`

```typescript
import { Position, Direction, SnakeGameState } from './types';
import { GRID_SIZE } from './constants';

export function moveSnake(state: SnakeGameState): SnakeGameState {
  if (state.isGameOver || state.isPaused) return state;

  const head = state.snake[0];
  let newHead: Position;

  // Calculer la nouvelle position de la tête
  switch (state.nextDirection) {
    case 'UP':
      newHead = { x: head.x, y: head.y - 1 };
      break;
    case 'DOWN':
      newHead = { x: head.x, y: head.y + 1 };
      break;
    case 'LEFT':
      newHead = { x: head.x - 1, y: head.y };
      break;
    case 'RIGHT':
      newHead = { x: head.x + 1, y: head.y };
      break;
  }

  // Vérifier collision avec les murs
  if (
    newHead.x < 0 ||
    newHead.x >= GRID_SIZE ||
    newHead.y < 0 ||
    newHead.y >= GRID_SIZE
  ) {
    return { ...state, isGameOver: true };
  }

  // Vérifier collision avec soi-même
  if (state.snake.some((segment) =>
    segment.x === newHead.x && segment.y === newHead.y
  )) {
    return { ...state, isGameOver: true };
  }

  const newSnake = [newHead, ...state.snake];

  // Vérifier si on mange la nourriture
  if (newHead.x === state.food.x && newHead.y === state.food.y) {
    return {
      ...state,
      snake: newSnake,
      food: generateFood(newSnake),
      score: state.score + 10,
      direction: state.nextDirection,
    };
  }

  // Mouvement normal (retirer la queue)
  newSnake.pop();

  return {
    ...state,
    snake: newSnake,
    direction: state.nextDirection,
  };
}

export function generateFood(snake: Position[]): Position {
  let food: Position;
  let isValid = false;

  while (!isValid) {
    food = {
      x: Math.floor(Math.random() * GRID_SIZE),
      y: Math.floor(Math.random() * GRID_SIZE),
    };

    isValid = !snake.some((segment) =>
      segment.x === food.x && segment.y === food.y
    );
  }

  return food!;
}

export function changeDirection(
  current: Direction,
  next: Direction
): Direction {
  // Empêcher les demi-tours
  const opposites: Record<Direction, Direction> = {
    UP: 'DOWN',
    DOWN: 'UP',
    LEFT: 'RIGHT',
    RIGHT: 'LEFT',
  };

  if (opposites[current] === next) {
    return current;
  }

  return next;
}
```

#### 5. Créer le composant du jeu `app/games/snake/page.tsx`

```tsx
'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, Play, Pause, RotateCcw } from 'lucide-react';
import Link from 'next/link';
import { useGameStore } from '@/stores/game-store';
import {
  moveSnake,
  changeDirection,
  INITIAL_STATE,
  GRID_SIZE,
  CELL_SIZE,
  COLORS,
  INITIAL_SPEED
} from '@/lib/games/snake';
import type { Direction, SnakeGameState } from '@/lib/games/snake/types';

export default function SnakePage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [gameState, setGameState] = useState<SnakeGameState>(INITIAL_STATE);
  const { updateHighScore, stats } = useGameStore();

  const highScore = stats.highScores['snake'] || 0;

  // Gérer les touches du clavier
  const handleKeyPress = useCallback((e: KeyboardEvent) => {
    if (gameState.isGameOver) return;

    let newDirection: Direction | null = null;

    switch (e.key) {
      case 'ArrowUp':
      case 'w':
        newDirection = 'UP';
        break;
      case 'ArrowDown':
      case 's':
        newDirection = 'DOWN';
        break;
      case 'ArrowLeft':
      case 'a':
        newDirection = 'LEFT';
        break;
      case 'ArrowRight':
      case 'd':
        newDirection = 'RIGHT';
        break;
      case ' ':
        togglePause();
        break;
    }

    if (newDirection) {
      e.preventDefault();
      setGameState((prev) => ({
        ...prev,
        nextDirection: changeDirection(prev.direction, newDirection!),
      }));
    }
  }, [gameState.isGameOver, gameState.direction]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [handleKeyPress]);

  // Game loop
  useEffect(() => {
    if (gameState.isGameOver || gameState.isPaused) return;

    const speed = INITIAL_SPEED - Math.floor(gameState.score / 50) * 10;
    const interval = setInterval(() => {
      setGameState((prev) => moveSnake(prev));
    }, Math.max(speed, 50));

    return () => clearInterval(interval);
  }, [gameState.isGameOver, gameState.isPaused, gameState.score]);

  // Sauvegarder le high score
  useEffect(() => {
    if (gameState.isGameOver && gameState.score > highScore) {
      updateHighScore('snake', gameState.score);
    }
  }, [gameState.isGameOver, gameState.score, highScore]);

  // Rendu du canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = COLORS.background;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Dessiner la grille
    ctx.strokeStyle = COLORS.grid;
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= GRID_SIZE; i++) {
      ctx.beginPath();
      ctx.moveTo(i * CELL_SIZE, 0);
      ctx.lineTo(i * CELL_SIZE, GRID_SIZE * CELL_SIZE);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(0, i * CELL_SIZE);
      ctx.lineTo(GRID_SIZE * CELL_SIZE, i * CELL_SIZE);
      ctx.stroke();
    }

    // Dessiner le serpent
    gameState.snake.forEach((segment, index) => {
      ctx.fillStyle = index === 0 ? COLORS.snake : `${COLORS.snake}CC`;
      ctx.fillRect(
        segment.x * CELL_SIZE + 1,
        segment.y * CELL_SIZE + 1,
        CELL_SIZE - 2,
        CELL_SIZE - 2
      );
    });

    // Dessiner la nourriture
    ctx.fillStyle = COLORS.food;
    ctx.beginPath();
    ctx.arc(
      gameState.food.x * CELL_SIZE + CELL_SIZE / 2,
      gameState.food.y * CELL_SIZE + CELL_SIZE / 2,
      CELL_SIZE / 2 - 2,
      0,
      2 * Math.PI
    );
    ctx.fill();
  }, [gameState]);

  const togglePause = () => {
    setGameState((prev) => ({ ...prev, isPaused: !prev.isPaused }));
  };

  const resetGame = () => {
    setGameState(INITIAL_STATE);
  };

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6 flex items-center justify-between">
          <Link href="/">
            <Button variant="ghost">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Retour
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">🐍 Snake</h1>
          <div className="w-24" />
        </div>

        <div className="grid md:grid-cols-[1fr,300px] gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="flex justify-center">
                <canvas
                  ref={canvasRef}
                  width={GRID_SIZE * CELL_SIZE}
                  height={GRID_SIZE * CELL_SIZE}
                  className="border-2 border-violet-500 rounded-lg"
                />
              </div>

              {gameState.isGameOver && (
                <div className="mt-4 text-center">
                  <p className="text-2xl font-bold text-red-500 mb-4">
                    Game Over!
                  </p>
                  <Button onClick={resetGame} size="lg">
                    <RotateCcw className="mr-2 h-4 w-4" />
                    Rejouer
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Score</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm text-muted-foreground">Score actuel</p>
                  <p className="text-4xl font-bold">{gameState.score}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Meilleur score</p>
                  <p className="text-2xl font-bold text-violet-500">
                    {Math.max(highScore, gameState.score)}
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Contrôles</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <Badge variant="outline">↑ / W</Badge>
                  <span>Haut</span>
                  <Badge variant="outline">↓ / S</Badge>
                  <span>Bas</span>
                  <Badge variant="outline">← / A</Badge>
                  <span>Gauche</span>
                  <Badge variant="outline">→ / D</Badge>
                  <span>Droite</span>
                  <Badge variant="outline">Espace</Badge>
                  <span>Pause</span>
                </div>

                <div className="pt-4 space-y-2">
                  <Button
                    onClick={togglePause}
                    className="w-full"
                    disabled={gameState.isGameOver}
                  >
                    {gameState.isPaused ? (
                      <>
                        <Play className="mr-2 h-4 w-4" />
                        Reprendre
                      </>
                    ) : (
                      <>
                        <Pause className="mr-2 h-4 w-4" />
                        Pause
                      </>
                    )}
                  </Button>

                  <Button
                    onClick={resetGame}
                    variant="outline"
                    className="w-full"
                  >
                    <RotateCcw className="mr-2 h-4 w-4" />
                    Recommencer
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </main>
  );
}
```

---

## 🎨 Templates de Code

### Template de Jeu Générique

Utilisez ce template pour créer un nouveau jeu rapidement:

```tsx
// app/games/[game-name]/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import Link from 'next/link';
import { ArrowLeft, Play, Pause, RotateCcw } from 'lucide-react';

export default function GamePage() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [score, setScore] = useState(0);

  // TODO: Implémenter la logique du jeu

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6 flex items-center justify-between">
          <Link href="/">
            <Button variant="ghost">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Retour
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">Nom du Jeu</h1>
          <div className="w-24" />
        </div>

        <Card className="p-6">
          {/* Zone de jeu */}
          <div className="min-h-[500px] flex items-center justify-center">
            <p>Zone de jeu ici</p>
          </div>

          {/* Contrôles */}
          <div className="mt-6 flex gap-4 justify-center">
            <Button onClick={() => setIsPlaying(!isPlaying)}>
              {isPlaying ? <Pause /> : <Play />}
              {isPlaying ? 'Pause' : 'Jouer'}
            </Button>
            <Button variant="outline">
              <RotateCcw className="mr-2" />
              Recommencer
            </Button>
          </div>
        </Card>
      </div>
    </main>
  );
}
```

---

## ✅ Best Practices

### 1. Performance

```typescript
// ❌ Mauvais
useEffect(() => {
  // Re-render à chaque frame
  setGameState(calculateNewState());
}, []);

// ✅ Bon
useEffect(() => {
  const interval = setInterval(() => {
    setGameState(prev => calculateNewState(prev));
  }, 16); // 60 FPS

  return () => clearInterval(interval);
}, []);
```

### 2. State Management

```typescript
// ❌ Mauvais - Multiples états
const [score, setScore] = useState(0);
const [isPlaying, setIsPlaying] = useState(false);
const [isPaused, setIsPaused] = useState(false);

// ✅ Bon - État unique
const [gameState, setGameState] = useState({
  score: 0,
  isPlaying: false,
  isPaused: false,
});
```

### 3. Cleanup

```typescript
useEffect(() => {
  const handleKeyPress = (e: KeyboardEvent) => {
    // Logique
  };

  window.addEventListener('keydown', handleKeyPress);

  // ✅ Toujours cleanup
  return () => {
    window.removeEventListener('keydown', handleKeyPress);
  };
}, []);
```

---

## 🧪 Testing et Debugging

### Test du mode offline

```bash
# 1. Build production
pnpm build

# 2. Serveur production
pnpm start

# 3. Ouvrir DevTools > Application > Service Workers
# 4. Cocher "Offline"
# 5. Recharger la page - le jeu doit fonctionner
```

### Debug Performance

```tsx
// Ajouter des logs de performance
useEffect(() => {
  const start = performance.now();

  // Logique du jeu

  const end = performance.now();
  if (end - start > 16) {
    console.warn(`Frame drop: ${end - start}ms`);
  }
}, []);
```

---

## 🚀 Déploiement

### Vercel (Recommandé)

```bash
# 1. Installer Vercel CLI
pnpm add -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel

# 4. Production
vercel --prod
```

### Netlify

```bash
# 1. Build
pnpm build

# 2. Netlify CLI
npx netlify-cli deploy

# 3. Production
npx netlify-cli deploy --prod
```

---

## 📖 Ressources Supplémentaires

- [Next.js Docs](https://nextjs.org/docs)
- [Shadcn UI](https://ui.shadcn.com)
- [Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [PWA Guide](https://web.dev/progressive-web-apps/)

---

**Bon développement! 🎮**
