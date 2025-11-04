#!/usr/bin/env python3
"""
Prompt Maître - Générateur Automatique de Prompts No Code
==========================================================
Architecture complète pour transformer du texte brut en prompts optimisés
avec double sortie : texte structuré + JSON standardisé
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class NoCodeTool(Enum):
    """Outils No Code reconnus par le système"""
    MAKE = "Make.com"
    ZAPIER = "Zapier"
    N8N = "n8n"
    AIRTABLE = "Airtable"
    NOTION = "Notion"
    BUBBLE = "Bubble"
    SLACK = "Slack"
    GOOGLE_SHEETS = "Google Sheets"
    WEBHOOKS = "Webhooks"
    API = "API"
    OPENAI = "OpenAI"
    ANTHROPIC = "Anthropic Claude"

    @classmethod
    def detect_tools(cls, text: str) -> List[str]:
        """Détecte les outils mentionnés dans le texte"""
        text_lower = text.lower()
        detected = []

        tool_keywords = {
            cls.MAKE: ["make", "make.com", "integromat"],
            cls.ZAPIER: ["zapier", "zap"],
            cls.N8N: ["n8n"],
            cls.AIRTABLE: ["airtable", "base"],
            cls.NOTION: ["notion", "database notion"],
            cls.BUBBLE: ["bubble", "bubble.io"],
            cls.SLACK: ["slack", "canal slack", "message slack"],
            cls.GOOGLE_SHEETS: ["google sheets", "sheets", "spreadsheet"],
            cls.WEBHOOKS: ["webhook", "api call"],
            cls.API: ["api", "endpoint"],
            cls.OPENAI: ["openai", "gpt", "chatgpt"],
            cls.ANTHROPIC: ["claude", "anthropic"],
        }

        for tool, keywords in tool_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.append(tool.value)

        return detected if detected else ["Automation Platform"]


class IntentType(Enum):
    """Types d'intentions détectables"""
    CONNECT = "connexion"
    AUTOMATE = "automatisation"
    NOTIFY = "notification"
    CREATE = "création"
    UPDATE = "mise à jour"
    SYNC = "synchronisation"
    TRANSFORM = "transformation"
    FILTER = "filtrage"
    ANALYZE = "analyse"
    GENERATE = "génération"


@dataclass
class SemanticAnalysis:
    """Résultat de l'analyse sémantique du texte brut"""
    intent: str
    action_verbs: List[str]
    tools: List[str]
    source: Optional[str]
    destination: Optional[str]
    trigger: Optional[str]
    context_keywords: List[str]
    complexity_score: int  # 1-5


@dataclass
class PromptStructure:
    """Structure standardisée d'un prompt optimisé"""
    role: str
    objective: str
    context: str
    tools: List[str]
    instructions: List[str]
    output_format: str
    tone: str
    constraints: Optional[List[str]] = None
    examples: Optional[List[str]] = None

    def to_json(self) -> str:
        """Convertit en JSON formaté"""
        data = asdict(self)
        # Supprimer les champs None
        data = {k: v for k, v in data.items() if v is not None}
        return json.dumps(data, ensure_ascii=False, indent=2)

    def to_text_prompt(self) -> str:
        """Génère le prompt en format texte optimisé"""
        sections = []

        # Rôle
        sections.append(f"# Rôle\n{self.role}\n")

        # Objectif
        sections.append(f"# Objectif\n{self.objective}\n")

        # Contexte
        if self.context:
            sections.append(f"# Contexte\n{self.context}\n")

        # Outils
        if self.tools:
            tools_list = "\n".join([f"- {tool}" for tool in self.tools])
            sections.append(f"# Outils concernés\n{tools_list}\n")

        # Instructions
        instructions_list = "\n".join([f"{i+1}. {instr}" for i, instr in enumerate(self.instructions)])
        sections.append(f"# Instructions\n{instructions_list}\n")

        # Contraintes
        if self.constraints:
            constraints_list = "\n".join([f"- {c}" for c in self.constraints])
            sections.append(f"# Contraintes\n{constraints_list}\n")

        # Format de sortie
        sections.append(f"# Format de sortie attendu\n{self.output_format}\n")

        # Exemples
        if self.examples:
            examples_list = "\n\n".join(self.examples)
            sections.append(f"# Exemples\n{examples_list}\n")

        # Ton
        sections.append(f"# Ton\n{self.tone}")

        return "\n".join(sections)


class PromptGenerator:
    """Moteur principal de génération de prompts"""

    def __init__(self):
        self.intent_patterns = {
            IntentType.CONNECT: ["connecter", "relier", "lier", "intégrer"],
            IntentType.AUTOMATE: ["automatiser", "automatique", "déclencher"],
            IntentType.NOTIFY: ["notifier", "alerter", "prévenir", "envoyer notification"],
            IntentType.CREATE: ["créer", "ajouter", "générer", "nouveau"],
            IntentType.UPDATE: ["mettre à jour", "modifier", "changer", "éditer"],
            IntentType.SYNC: ["synchroniser", "synchro", "garder à jour"],
            IntentType.TRANSFORM: ["transformer", "convertir", "adapter"],
            IntentType.FILTER: ["filtrer", "trier", "sélectionner"],
            IntentType.ANALYZE: ["analyser", "examiner", "étudier"],
            IntentType.GENERATE: ["générer", "produire", "construire"],
        }

    def analyze_text(self, raw_text: str) -> SemanticAnalysis:
        """
        Étape 1 & 2: Lecture et extraction sémantique
        Analyse le texte brut pour extraire l'intention et le contexte
        """
        text_lower = raw_text.lower()

        # Détecter l'intention principale
        detected_intents = []
        for intent, patterns in self.intent_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                detected_intents.append(intent.value)

        primary_intent = detected_intents[0] if detected_intents else "automatisation"

        # Extraire les verbes d'action
        action_verbs = self._extract_action_verbs(raw_text)

        # Détecter les outils
        tools = NoCodeTool.detect_tools(raw_text)

        # Détecter source et destination
        source, destination = self._detect_source_destination(raw_text, tools)

        # Détecter le trigger
        trigger = self._detect_trigger(raw_text)

        # Extraire mots-clés contextuels
        context_keywords = self._extract_context_keywords(raw_text)

        # Calculer score de complexité
        complexity = self._calculate_complexity(raw_text, tools, detected_intents)

        return SemanticAnalysis(
            intent=primary_intent,
            action_verbs=action_verbs,
            tools=tools,
            source=source,
            destination=destination,
            trigger=trigger,
            context_keywords=context_keywords,
            complexity_score=complexity
        )

    def generate_prompt(self, raw_text: str) -> PromptStructure:
        """
        Étape 3: Génération du prompt optimisé
        Transforme l'analyse sémantique en prompt structuré
        """
        # Analyser le texte
        analysis = self.analyze_text(raw_text)

        # Construire le rôle
        role = self._build_role(analysis)

        # Construire l'objectif
        objective = self._build_objective(analysis, raw_text)

        # Construire le contexte
        context = self._build_context(analysis)

        # Générer les instructions
        instructions = self._build_instructions(analysis)

        # Définir le format de sortie
        output_format = self._build_output_format(analysis)

        # Définir le ton
        tone = self._determine_tone(analysis)

        # Ajouter contraintes si nécessaire
        constraints = self._build_constraints(analysis)

        # Ajouter exemples si pertinent
        examples = self._build_examples(analysis)

        return PromptStructure(
            role=role,
            objective=objective,
            context=context,
            tools=analysis.tools,
            instructions=instructions,
            output_format=output_format,
            tone=tone,
            constraints=constraints if constraints else None,
            examples=examples if examples else None
        )

    def _extract_action_verbs(self, text: str) -> List[str]:
        """Extrait les verbes d'action du texte"""
        action_verbs = [
            "connecter", "créer", "envoyer", "recevoir", "transformer",
            "filtrer", "analyser", "notifier", "synchroniser", "automatiser",
            "générer", "mettre à jour", "supprimer", "archiver"
        ]
        found = []
        text_lower = text.lower()
        for verb in action_verbs:
            if verb in text_lower:
                found.append(verb)
        return found[:5]  # Limiter à 5 verbes

    def _detect_source_destination(self, text: str, tools: List[str]) -> Tuple[Optional[str], Optional[str]]:
        """Détecte la source et la destination dans le flux"""
        # Patterns pour détecter source -> destination
        patterns = [
            r"(?:de|depuis|from)\s+(\w+)\s+(?:vers|à|to)\s+(\w+)",
            r"(\w+)\s+(?:vers|à|to)\s+(\w+)",
            r"connecter\s+(\w+)\s+(?:à|avec)\s+(\w+)"
        ]

        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).capitalize(), match.group(2).capitalize()

        # Si on a détecté au moins 2 outils, le premier est source, le second destination
        if len(tools) >= 2:
            return tools[0], tools[1]

        return None, None

    def _detect_trigger(self, text: str) -> Optional[str]:
        """Détecte l'événement déclencheur"""
        trigger_patterns = {
            "nouveau": "nouvel enregistrement/élément créé",
            "modif": "élément modifié",
            "supprim": "élément supprimé",
            "ajout": "élément ajouté",
            "envoi": "message envoyé",
            "réception": "message reçu",
            "planif": "événement planifié",
        }

        text_lower = text.lower()
        for keyword, trigger in trigger_patterns.items():
            if keyword in text_lower:
                return trigger

        return "événement spécifique"

    def _extract_context_keywords(self, text: str) -> List[str]:
        """Extrait les mots-clés contextuels importants"""
        # Supprimer les stop words et extraire les mots significatifs
        stop_words = {"le", "la", "les", "un", "une", "des", "pour", "dans", "avec", "être", "avoir"}
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        return list(set(keywords))[:10]  # Top 10 mots-clés uniques

    def _calculate_complexity(self, text: str, tools: List[str], intents: List[str]) -> int:
        """Calcule un score de complexité (1-5)"""
        score = 1

        # Plus d'outils = plus complexe
        if len(tools) > 2:
            score += 1
        if len(tools) > 4:
            score += 1

        # Multiples intentions = plus complexe
        if len(intents) > 1:
            score += 1

        # Longueur du texte
        if len(text) > 100:
            score += 1

        return min(score, 5)

    def _build_role(self, analysis: SemanticAnalysis) -> str:
        """Construit le rôle approprié selon le contexte"""
        if "OpenAI" in analysis.tools or "Anthropic Claude" in analysis.tools:
            return "Tu es un expert en automatisation No Code spécialisé dans l'intégration d'IA générative, avec une expertise approfondie en ingénierie de prompt et architecture de workflows intelligents."
        elif len(analysis.tools) > 2:
            return "Tu es un architecte en automatisation No Code expert en intégrations complexes multi-plateformes, capable de concevoir des workflows robustes et scalables."
        else:
            return f"Tu es un expert en automatisation No Code spécialisé en {analysis.intent}, avec une maîtrise avancée des outils d'intégration modernes."

    def _build_objective(self, analysis: SemanticAnalysis, raw_text: str) -> str:
        """Construit l'objectif clair et précis"""
        if analysis.source and analysis.destination:
            return f"Concevoir une automatisation pour {analysis.intent} entre {analysis.source} et {analysis.destination}, déclenchée par {analysis.trigger}."
        else:
            # Reformuler le texte brut de manière plus structurée
            return f"Créer une solution d'automatisation pour : {raw_text}"

    def _build_context(self, analysis: SemanticAnalysis) -> str:
        """Construit le contexte pertinent"""
        context_parts = []

        if analysis.complexity_score >= 3:
            context_parts.append("Ce workflow nécessite une architecture robuste avec gestion d'erreurs.")

        if len(analysis.tools) > 0:
            tools_str = ", ".join(analysis.tools)
            context_parts.append(f"Outils disponibles : {tools_str}")

        if analysis.trigger:
            context_parts.append(f"Déclencheur : {analysis.trigger}")

        context_parts.append("L'utilisateur recherche une solution No Code sans développement personnalisé.")

        return " ".join(context_parts)

    def _build_instructions(self, analysis: SemanticAnalysis) -> List[str]:
        """Génère les instructions étape par étape"""
        instructions = []

        # Instruction 1: Configuration du déclencheur
        if analysis.trigger:
            instructions.append(f"Configure le déclencheur : {analysis.trigger} dans l'outil source")
        else:
            instructions.append("Identifie et configure l'événement déclencheur approprié")

        # Instruction 2: Récupération des données
        if analysis.source:
            instructions.append(f"Récupère les données pertinentes depuis {analysis.source}")
        else:
            instructions.append("Récupère et structure les données d'entrée")

        # Instruction 3: Transformation si nécessaire
        if "transform" in analysis.intent or len(analysis.tools) > 2:
            instructions.append("Transforme et formate les données selon les besoins de la destination")

        # Instruction 4: Filtrage/conditions
        if "filter" in analysis.intent or analysis.complexity_score >= 3:
            instructions.append("Applique les filtres et conditions nécessaires")

        # Instruction 5: Action finale
        if analysis.destination:
            instructions.append(f"Envoie les données formatées vers {analysis.destination}")
        else:
            instructions.append("Exécute l'action finale configurée")

        # Instruction 6: Gestion d'erreurs
        if analysis.complexity_score >= 3:
            instructions.append("Implémente la gestion d'erreurs et les notifications en cas d'échec")

        # Instruction 7: Test
        instructions.append("Teste le workflow avec des données réelles et vérifie tous les cas d'usage")

        return instructions

    def _build_output_format(self, analysis: SemanticAnalysis) -> str:
        """Définit le format de sortie attendu"""
        if analysis.complexity_score >= 4:
            return """Fournis un guide complet structuré comme suit :
1. Architecture du workflow (schéma visuel en texte)
2. Configuration détaillée étape par étape
3. Paramètres et mappings de champs
4. Gestion d'erreurs et cas limites
5. Tests de validation recommandés"""
        else:
            return """Fournis un guide pratique incluant :
1. Les étapes de configuration
2. Les paramètres clés
3. Un exemple de test"""

    def _determine_tone(self, analysis: SemanticAnalysis) -> str:
        """Détermine le ton approprié"""
        if analysis.complexity_score >= 4:
            return "Professionnel, technique et exhaustif. Utilise une terminologie précise adaptée aux experts en automatisation."
        elif analysis.complexity_score >= 2:
            return "Pédagogique et structuré. Équilibre entre précision technique et accessibilité."
        else:
            return "Clair, direct et accessible. Privilégie la simplicité sans sacrifier la précision."

    def _build_constraints(self, analysis: SemanticAnalysis) -> List[str]:
        """Construit les contraintes si nécessaire"""
        constraints = []

        if "API" in analysis.tools:
            constraints.append("Respecter les limites de taux d'API (rate limits)")

        if analysis.complexity_score >= 3:
            constraints.append("Assurer la traçabilité de toutes les opérations")
            constraints.append("Implémenter des mécanismes de retry pour les opérations critiques")

        if "Airtable" in analysis.tools or "Notion" in analysis.tools:
            constraints.append("Respecter la structure des bases de données existantes")

        return constraints if constraints else None

    def _build_examples(self, analysis: SemanticAnalysis) -> List[str]:
        """Génère des exemples si pertinent"""
        if analysis.complexity_score <= 2:
            return None

        examples = []

        if analysis.source and analysis.destination:
            examples.append(f"""Exemple de flux de données :
{analysis.source} (nouveau record) → Transformation → {analysis.destination} (création)
Données : {{nom, email, statut}} → Validation → Message Slack formaté""")

        return examples if examples else None


def generate_from_text(raw_text: str) -> Dict[str, str]:
    """
    Fonction principale : transforme un texte brut en prompt optimisé

    Args:
        raw_text: Texte brut décrivant le besoin

    Returns:
        Dict contenant 'text_prompt' et 'json_prompt'
    """
    generator = PromptGenerator()
    prompt_structure = generator.generate_prompt(raw_text)

    return {
        "text_prompt": prompt_structure.to_text_prompt(),
        "json_prompt": prompt_structure.to_json(),
        "analysis": prompt_structure  # Pour debugging/inspection
    }


# Interface CLI pour tests rapides
if __name__ == "__main__":
    print("=== Prompt Maître - Générateur de Prompts No Code ===\n")

    # Exemple de démonstration
    example_input = "Je veux connecter Airtable à Slack pour être notifié quand un nouvel enregistrement est ajouté."

    print(f"📥 Entrée (texte brut) :\n{example_input}\n")
    print("=" * 80)

    result = generate_from_text(example_input)

    print("\n📄 SORTIE 1 : PROMPT TEXTE OPTIMISÉ")
    print("=" * 80)
    print(result["text_prompt"])

    print("\n\n📋 SORTIE 2 : JSON STRUCTURÉ")
    print("=" * 80)
    print(result["json_prompt"])

    print("\n\n✅ Génération terminée avec succès!")
