#!/usr/bin/env python3
"""
Tests pour l'API Prompt Maître
===============================
Tests unitaires et d'intégration
"""

import pytest
import json
from fastapi.testclient import TestClient
from api_server import app
from prompt_generator import generate_from_text, PromptGenerator, SemanticAnalysis

# Créer un client de test
client = TestClient(app)


class TestPromptGenerator:
    """Tests du moteur de génération"""

    def test_simple_connection(self):
        """Test : connexion simple entre deux outils"""
        text = "Je veux connecter Airtable à Slack pour être notifié quand un nouvel enregistrement est ajouté."
        result = generate_from_text(text)

        assert "text_prompt" in result
        assert "json_prompt" in result
        assert len(result["text_prompt"]) > 100
        assert "Airtable" in result["text_prompt"]
        assert "Slack" in result["text_prompt"]

    def test_complex_workflow(self):
        """Test : workflow complexe avec multiple outils"""
        text = """
        Créer une automatisation qui récupère les nouveaux leads depuis Google Sheets,
        vérifie leur validité avec une API, enrichit les données via OpenAI,
        puis crée un enregistrement dans Airtable et envoie une notification Slack.
        """
        result = generate_from_text(text)

        analysis = result["analysis"]
        assert analysis.complexity_score >= 4
        assert "OpenAI" in analysis.tools
        assert "Google Sheets" in analysis.tools

    def test_json_validity(self):
        """Test : validation du JSON généré"""
        text = "Synchroniser Notion avec Airtable"
        result = generate_from_text(text)

        # Vérifier que le JSON est valide
        json_data = json.loads(result["json_prompt"])

        # Vérifier les champs requis
        required_fields = ["role", "objective", "context", "tools", "instructions", "output_format", "tone"]
        for field in required_fields:
            assert field in json_data, f"Champ requis manquant : {field}"

        # Vérifier les types
        assert isinstance(json_data["tools"], list)
        assert isinstance(json_data["instructions"], list)
        assert len(json_data["instructions"]) >= 3

    def test_tool_detection(self):
        """Test : détection des outils"""
        generator = PromptGenerator()

        test_cases = [
            ("connecter airtable à slack", ["Airtable", "Slack"]),
            ("automatiser avec make et notion", ["Make.com", "Notion"]),
            ("utiliser openai pour analyser", ["OpenAI"]),
            ("envoyer vers google sheets", ["Google Sheets"]),
        ]

        for text, expected_tools in test_cases:
            analysis = generator.analyze_text(text)
            for tool in expected_tools:
                assert tool in analysis.tools, f"Outil {tool} non détecté dans '{text}'"

    def test_intent_detection(self):
        """Test : détection des intentions"""
        generator = PromptGenerator()

        test_cases = [
            ("connecter deux outils", "connexion"),
            ("automatiser l'envoi", "automatisation"),
            ("être notifié quand", "notification"),
            ("créer un enregistrement", "création"),
            ("synchroniser les données", "synchronisation"),
        ]

        for text, expected_intent in test_cases:
            analysis = generator.analyze_text(text)
            assert analysis.intent == expected_intent, f"Intention incorrecte pour '{text}'"

    def test_complexity_scoring(self):
        """Test : calcul du score de complexité"""
        generator = PromptGenerator()

        # Simple
        simple_text = "Connecter Airtable à Slack"
        simple_analysis = generator.analyze_text(simple_text)
        assert simple_analysis.complexity_score <= 2

        # Complexe
        complex_text = """
        Automatisation avec Google Sheets, API, OpenAI, Airtable, Slack
        incluant transformation, validation, et gestion d'erreurs
        """
        complex_analysis = generator.analyze_text(complex_text)
        assert complex_analysis.complexity_score >= 4


class TestAPI:
    """Tests des endpoints de l'API"""

    def test_root_endpoint(self):
        """Test : endpoint racine"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self):
        """Test : health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_generate_endpoint_success(self):
        """Test : génération réussie"""
        payload = {
            "raw_text": "Je veux connecter Airtable à Slack pour être notifié quand un nouvel enregistrement est ajouté."
        }
        response = client.post("/generate", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert "text_prompt" in data
        assert "json_prompt" in data
        assert "metadata" in data
        assert data["metadata"]["detected_tools"] == ["Airtable", "Slack"]

    def test_generate_endpoint_validation(self):
        """Test : validation des entrées"""
        # Texte trop court
        response = client.post("/generate", json={"raw_text": "test"})
        assert response.status_code == 422  # Validation error

        # Texte vide
        response = client.post("/generate", json={"raw_text": ""})
        assert response.status_code == 422

        # Champ manquant
        response = client.post("/generate", json={})
        assert response.status_code == 422

    def test_generate_endpoint_metadata(self):
        """Test : métadonnées de génération"""
        payload = {
            "raw_text": "Automatiser l'envoi d'emails depuis Google Sheets vers des clients"
        }
        response = client.post("/generate", json=payload)
        data = response.json()

        metadata = data["metadata"]
        assert "generation_time_seconds" in metadata
        assert "complexity_score" in metadata
        assert "detected_intent" in metadata
        assert metadata["generation_time_seconds"] > 0

    def test_tools_endpoint(self):
        """Test : liste des outils supportés"""
        response = client.get("/tools")
        assert response.status_code == 200
        data = response.json()

        assert "supported_tools" in data
        assert "Make.com" in data["supported_tools"]
        assert "Airtable" in data["supported_tools"]
        assert data["total"] >= 10

    def test_intents_endpoint(self):
        """Test : liste des intentions"""
        response = client.get("/intents")
        assert response.status_code == 200
        data = response.json()

        assert "supported_intents" in data
        intents = data["supported_intents"]
        assert len(intents) >= 8

        # Vérifier la structure
        first_intent = intents[0]
        assert "name" in first_intent
        assert "keywords" in first_intent

    def test_schema_endpoint(self):
        """Test : schéma JSON"""
        response = client.get("/schema")
        assert response.status_code == 200
        data = response.json()

        assert "schema" in data
        schema = data["schema"]
        assert "properties" in schema
        assert "required" in schema

    def test_examples_endpoint(self):
        """Test : exemples d'utilisation"""
        response = client.get("/examples")
        assert response.status_code == 200
        data = response.json()

        assert "examples" in data
        examples = data["examples"]
        assert len(examples) >= 3

        # Vérifier la structure des exemples
        first_example = examples[0]
        assert "input" in first_example
        assert "description" in first_example
        assert "complexity" in first_example

    def test_batch_endpoint(self):
        """Test : génération en batch"""
        payload = [
            {"raw_text": "Connecter Airtable à Slack"},
            {"raw_text": "Automatiser emails Google Sheets"},
            {"raw_text": "Synchroniser Notion et Airtable"}
        ]
        response = client.post("/batch", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert "results" in data
        assert len(data["results"]) == 3

        # Vérifier que toutes les générations ont réussi
        for result in data["results"]:
            assert result["status"] == "success"
            assert "text_prompt" in result

    def test_batch_endpoint_limit(self):
        """Test : limite du batch"""
        # Créer plus de 10 requêtes
        payload = [{"raw_text": f"Test {i}"} for i in range(11)]
        response = client.post("/batch", json=payload)

        assert response.status_code == 400
        assert "Maximum 10 requêtes" in response.json()["detail"]

    def test_cors_headers(self):
        """Test : headers CORS"""
        response = client.options("/generate")
        assert "access-control-allow-origin" in response.headers


class TestEdgeCases:
    """Tests des cas limites"""

    def test_multilingual_input(self):
        """Test : entrée en anglais"""
        text = "Connect Airtable to Slack and send notifications"
        result = generate_from_text(text)

        assert "Airtable" in result["text_prompt"]
        assert "Slack" in result["text_prompt"]

    def test_very_short_input(self):
        """Test : texte très court mais valide"""
        text = "Airtable to Slack notification"
        result = generate_from_text(text)

        assert len(result["text_prompt"]) > 100

    def test_no_tools_detected(self):
        """Test : aucun outil explicitement mentionné"""
        text = "Je veux automatiser l'envoi de messages quand quelque chose arrive"
        result = generate_from_text(text)

        # Devrait quand même générer un prompt valide
        assert len(result["text_prompt"]) > 0
        analysis = result["analysis"]
        assert "Automation Platform" in analysis.tools

    def test_multiple_intents(self):
        """Test : multiples intentions"""
        text = "Connecter, synchroniser et transformer les données entre plusieurs outils"
        result = generate_from_text(text)

        analysis = result["analysis"]
        # Au moins une intention devrait être détectée
        assert len(analysis.intent) > 0

    def test_special_characters(self):
        """Test : caractères spéciaux"""
        text = "Connecter Airtable → Slack avec émojis 🚀 et caractères spéciaux (test)"
        result = generate_from_text(text)

        # Ne devrait pas crasher
        assert "text_prompt" in result
        assert "json_prompt" in result


class TestPerformance:
    """Tests de performance"""

    def test_generation_time(self):
        """Test : temps de génération acceptable"""
        import time

        text = "Connecter Airtable à Slack pour notifications"

        start = time.time()
        result = generate_from_text(text)
        duration = time.time() - start

        # Devrait prendre moins de 1 seconde
        assert duration < 1.0, f"Génération trop lente : {duration}s"

    def test_api_response_time(self):
        """Test : temps de réponse API"""
        payload = {"raw_text": "Automatiser avec Make et Notion"}

        response = client.post("/generate", json=payload)
        assert response.status_code == 200

        # Vérifier le temps dans les métadonnées
        metadata = response.json()["metadata"]
        assert metadata["generation_time_seconds"] < 1.0


# Fonction pour exécuter tous les tests
def run_all_tests():
    """Exécute tous les tests"""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    print("=" * 80)
    print("🧪 Exécution des tests du Générateur de Prompts No Code")
    print("=" * 80)
    run_all_tests()
