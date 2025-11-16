# 🎮 Démarrage Rapide - Plateforme de Jeux Offline

## ⚡ Installation Express (5 minutes)

### Option 1: Script Automatique 🚀

```bash
# Dans le dossier Prompt-engeneer/
./setup-games-platform.sh
```

Attendez 5-10 minutes et c'est prêt! ✨

### Option 2: Commandes Manuelles

```bash
# 1. Créer le projet
npx create-next-app@latest games-platform --typescript --tailwind --app --use-pnpm

cd games-platform

# 2. Initialiser Shadcn
npx shadcn-ui@latest init -d

# 3. Ajouter composants
npx shadcn-ui@latest add button card dialog badge toast -y

# 4. Dépendances
pnpm add zustand framer-motion lucide-react next-pwa
```

---

## 🏃 Lancer le Projet

```bash
cd games-platform

# Développement
pnpm dev

# Ouvrir http://localhost:3000
```

---

## 📁 Structure Créée

```
games-platform/
├── app/
│   ├── games/
│   │   ├── snake/          # 🐍 Snake
│   │   ├── tic-tac-toe/    # ⭕ Tic-Tac-Toe
│   │   ├── memory/         # 🃏 Memory
│   │   └── 2048/           # 🔢 2048
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/                 # Shadcn components
│   ├── games/              # Game components
│   └── layout/             # Layout components
├── lib/
│   ├── games/              # Game logic
│   └── storage/            # LocalStorage/IndexedDB
└── stores/                 # Zustand stores
```

---

## 🎯 Étapes de Développement

### 1️⃣ Page d'Accueil (1h)

Créer `app/page.tsx`:

```tsx
import { GameCard } from '@/components/games/GameCard';

export default function HomePage() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-4xl font-bold text-center mb-8">
        🎮 Jeux Offline
      </h1>
      {/* Liste des jeux */}
    </div>
  );
}
```

### 2️⃣ Premier Jeu: Snake (4h)

```bash
# Créer la structure
mkdir -p app/games/snake
mkdir -p lib/games/snake

# Fichiers à créer:
# - app/games/snake/page.tsx       (UI)
# - lib/games/snake/engine.ts      (Logique)
# - lib/games/snake/types.ts       (Types)
# - lib/games/snake/constants.ts   (Config)
```

Copier le code depuis `GAMES_DEVELOPMENT_GUIDE.md` section "Snake"

### 3️⃣ Tests Offline (30min)

```bash
# Build production
pnpm build

# Test en local
pnpm start

# Ouvrir DevTools > Application > Offline ✓
```

---

## 🎨 Personnalisation Rapide

### Changer les Couleurs

Éditer `app/globals.css`:

```css
:root {
  --primary: 262 83% 58%;        /* Violet → votre couleur */
  --accent: 142 71% 45%;         /* Vert → votre couleur */
}
```

### Ajouter un Jeu

1. Copier le template depuis `GAMES_DEVELOPMENT_GUIDE.md`
2. Créer `app/games/[nom]/page.tsx`
3. Ajouter la logique dans `lib/games/[nom]/`
4. Ajouter dans `lib/games-config.ts`

---

## 🐛 Problèmes Courants

### Le build échoue

```bash
# Nettoyer et rebuild
rm -rf .next node_modules
pnpm install
pnpm build
```

### Shadcn ne s'installe pas

```bash
# Vérifier la config
cat components.json

# Réinitialiser
npx shadcn-ui@latest init
```

### PWA ne fonctionne pas

```bash
# Vérifier next.config.js
# S'assurer que next-pwa est installé
pnpm add next-pwa

# Build production nécessaire
pnpm build && pnpm start
```

---

## 📚 Documentation Complète

| Document | Description |
|----------|-------------|
| `OFFLINE_GAMES_ARCHITECTURE.md` | Architecture complète du projet |
| `GAMES_DEVELOPMENT_GUIDE.md` | Guide de développement détaillé |
| `README_GAMES.md` | Documentation du projet games-platform |

---

## 🎯 Checklist de Démarrage

- [ ] Script `setup-games-platform.sh` exécuté
- [ ] Projet `games-platform/` créé
- [ ] `pnpm dev` fonctionne
- [ ] Page d'accueil affichée
- [ ] Shadcn UI installé
- [ ] PWA configuré
- [ ] Premier jeu (Snake) implémenté
- [ ] Mode offline testé
- [ ] Build production réussi

---

## 🚀 Prochaines Étapes

1. **Jour 1**: Setup + Page d'accueil
2. **Jour 2-3**: Développer Snake
3. **Jour 4**: Développer Tic-Tac-Toe
4. **Jour 5**: Développer Memory
5. **Jour 6-7**: Développer 2048
6. **Jour 8**: Polish + Tests
7. **Jour 9**: Déploiement

---

## 💬 Support

- Consulter `GAMES_DEVELOPMENT_GUIDE.md` pour les détails
- Vérifier les templates de code
- Tester en mode offline avant déploiement

---

**Bon développement! 🎮✨**

---

## 🔥 Commandes Essentielles

```bash
# Développement
pnpm dev                    # Lancer le serveur (localhost:3000)

# Build
pnpm build                  # Build production
pnpm start                  # Serveur production

# Shadcn
npx shadcn-ui@latest add button  # Ajouter un composant

# Git
git add .
git commit -m "feat: add offline games platform"
git push

# Déploiement
vercel                      # Deploy sur Vercel
# OU
npx netlify-cli deploy      # Deploy sur Netlify
```

---

**Version**: 1.0.0
**Date**: 2025-11-16
**Author**: Claude
