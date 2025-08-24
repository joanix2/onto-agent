import json
import pytest
from jsonschema import validate
from src.features.ontology_triplets.ontology_triplets_agent import generate_ontology_triplets

class TestOntologyTriplets:
    @pytest.fixture(autouse=True)
    def setup(self, setup_environment):
        """Configure l'environnement de test avec le modèle LLM"""
        self.model = setup_environment
        
        # Charger le schéma JSON
        with open('src/core/ontology/schema.json', 'r') as f:
            self.schema = json.load(f)
            
        return self.model

    def test_generate_ontology_triplets(self):
        """Test la génération de triplets d'ontologie avec la structure attendue"""
        # Données de test
        dms_backlog = [
            "Les attributs sont de type int, string, bool",
            "Les modèles sont un ensemble d'attributs",
            "Les vues affichent les données du modèle",
            "Les contrôleurs gèrent les interactions entre le modèle et les vues",
            "Les vues et les contrôleurs sont liés à un modèle spécifique",
            "Le contrôleur modifie les données du modèle",
            "Les vues permettent de visualiser les modifications du modèle",
            "Il peut y avoir plusieurs instances de modèles, vues et contrôleurs"
        ]
        
        # Appel de la fonction à tester
        result = generate_ontology_triplets(self.model, dms_backlog, lang="Français")[0]
        
        # Afficher le résultat pour le debug
        print("\nRésultat obtenu:", json.dumps(result, indent=2, ensure_ascii=False))
        
        # Valider la structure avec le schéma JSON
        validate(instance=result, schema=self.schema)