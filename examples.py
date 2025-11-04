#!/usr/bin/env python3
"""
Exemples d'utilisation du Générateur de Prompts No Code
========================================================
Démonstration avec différents cas d'usage
"""

from prompt_generator import generate_from_text


def example_1_simple_connection():
    """Exemple 1 : Connexion simple entre deux outils"""
    print("\n" + "="*80)
    print("EXEMPLE 1 : Connexion simple Airtable → Slack")
    print("="*80)

    raw_text = "Je veux connecter Airtable à Slack pour être notifié quand un nouvel enregistrement est ajouté."

    print(f"\n📥 Texte brut d'entrée :\n{raw_text}\n")

    result = generate_from_text(raw_text)

    print("\n📄 PROMPT TEXTE GÉNÉRÉ :")
    print("-" * 80)
    print(result["text_prompt"])

    print("\n\n📋 JSON GÉNÉRÉ :")
    print("-" * 80)
    print(result["json_prompt"])


def example_2_complex_workflow():
    """Exemple 2 : Workflow complexe multi-étapes"""
    print("\n" + "="*80)
    print("EXEMPLE 2 : Workflow complexe avec transformation de données")
    print("="*80)

    raw_text = """
    Créer une automatisation qui récupère les nouveaux leads depuis Google Sheets,
    vérifie leur validité avec une API, enrichit les données via OpenAI,
    puis crée un enregistrement dans Airtable et envoie une notification Slack
    avec un résumé généré par IA.
    """

    print(f"\n📥 Texte brut d'entrée :\n{raw_text}\n")

    result = generate_from_text(raw_text)

    print("\n📄 PROMPT TEXTE GÉNÉRÉ :")
    print("-" * 80)
    print(result["text_prompt"])

    print("\n\n📋 JSON GÉNÉRÉ :")
    print("-" * 80)
    print(result["json_prompt"])


def example_3_ai_integration():
    """Exemple 3 : Intégration IA générative"""
    print("\n" + "="*80)
    print("EXEMPLE 3 : Intégration Claude pour analyse de contenu")
    print("="*80)

    raw_text = """
    Automatiser l'analyse des feedbacks clients stockés dans Notion
    en utilisant Claude pour catégoriser les sentiments et extraire
    les insights clés, puis mettre à jour une base Airtable avec les résultats.
    """

    print(f"\n📥 Texte brut d'entrée :\n{raw_text}\n")

    result = generate_from_text(raw_text)

    print("\n📄 PROMPT TEXTE GÉNÉRÉ :")
    print("-" * 80)
    print(result["text_prompt"])

    print("\n\n📋 JSON GÉNÉRÉ :")
    print("-" * 80)
    print(result["json_prompt"])


def example_4_sync_workflow():
    """Exemple 4 : Synchronisation bidirectionnelle"""
    print("\n" + "="*80)
    print("EXEMPLE 4 : Synchronisation bidirectionnelle")
    print("="*80)

    raw_text = """
    Synchroniser automatiquement les tâches entre Notion et Airtable
    dans les deux sens, en temps réel.
    """

    print(f"\n📥 Texte brut d'entrée :\n{raw_text}\n")

    result = generate_from_text(raw_text)

    print("\n📄 PROMPT TEXTE GÉNÉRÉ :")
    print("-" * 80)
    print(result["text_prompt"])

    print("\n\n📋 JSON GÉNÉRÉ :")
    print("-" * 80)
    print(result["json_prompt"])


def example_5_webhook_api():
    """Exemple 5 : Webhook et API personnalisée"""
    print("\n" + "="*80)
    print("EXEMPLE 5 : Webhook vers API personnalisée")
    print("="*80)

    raw_text = """
    Recevoir des webhooks d'un formulaire, transformer les données,
    et envoyer vers une API personnalisée avec gestion d'erreurs.
    """

    print(f"\n📥 Texte brut d'entrée :\n{raw_text}\n")

    result = generate_from_text(raw_text)

    print("\n📄 PROMPT TEXTE GÉNÉRÉ :")
    print("-" * 80)
    print(result["text_prompt"])

    print("\n\n📋 JSON GÉNÉRÉ :")
    print("-" * 80)
    print(result["json_prompt"])


def run_all_examples():
    """Exécute tous les exemples"""
    print("\n" + "="*80)
    print("🚀 DÉMONSTRATION DU GÉNÉRATEUR DE PROMPTS NO CODE")
    print("="*80)

    example_1_simple_connection()
    example_2_complex_workflow()
    example_3_ai_integration()
    example_4_sync_workflow()
    example_5_webhook_api()

    print("\n" + "="*80)
    print("✅ Tous les exemples ont été générés avec succès!")
    print("="*80)


if __name__ == "__main__":
    run_all_examples()
