import pytest

from src.core.llms import get_completion
from src.features.ontology_triplets.ontology_triplets_agent import generate_ontology_triplets

class TestOntologyTriplets:
    @pytest.fixture(autouse=True)
    def setup(self, setup_environment):
        """Configure l'environnement de test avec le modèle LLM"""
        self.model = setup_environment
        return self.model

    def test_generate_ontology_triplets(self):
        """Test la génération de triplets d'ontologie avec la structure attendue"""
        # Données de test
        system_data = {}
        dms_backlog = [
            "Créer une ontologie pour un système universitaire avec des étudiants, des professeurs et des cours"
        ]
        
        # Appel de la fonction à tester
        result = generate_ontology_triplets(self.model, dms_backlog, lang="Français")[0]

        # Vérification de la structure du résultat
        assert isinstance(result, dict), "Le résultat doit être un dictionnaire"
        
        # Vérification des clés requises
        required_keys = {"classes", "object_properties", "data_properties", "individuals", "axioms"}
        assert set(result.keys()) == required_keys, f"Le résultat doit contenir exactement les clés: {required_keys}"
        
        # Vérification des classes
        assert isinstance(result["classes"], list), "classes doit être une liste"
        assert all(isinstance(c, str) for c in result["classes"]), "Toutes les classes doivent être des chaînes"
        
        # Vérification des object_properties
        assert isinstance(result["object_properties"], list), "object_properties doit être une liste"
        for prop in result["object_properties"]:
            assert isinstance(prop, dict), "Chaque object_property doit être un dictionnaire"
            assert set(prop.keys()) == {"name", "domain", "range"}, "Chaque object_property doit avoir name, domain et range"
            assert all(isinstance(prop[k], str) for k in prop), "Toutes les valeurs doivent être des chaînes"
        
        # Vérification des data_properties
        assert isinstance(result["data_properties"], list), "data_properties doit être une liste"
        for prop in result["data_properties"]:
            assert isinstance(prop, dict), "Chaque data_property doit être un dictionnaire"
            assert set(prop.keys()) == {"name", "domain", "range"}, "Chaque data_property doit avoir name, domain et range"
            assert all(isinstance(prop[k], str) for k in prop), "Toutes les valeurs doivent être des chaînes"
        
        # Vérification des individuals
        assert isinstance(result["individuals"], list), "individuals doit être une liste"
        assert all(isinstance(i, str) for i in result["individuals"]), "Tous les individuals doivent être des chaînes"
        
        # Vérification des axioms
        assert isinstance(result["axioms"], list), "axioms doit être une liste"
        for axiom in result["axioms"]:
            assert isinstance(axiom, dict), "Chaque axiom doit être un dictionnaire"
            assert "type" in axiom, "Chaque axiom doit avoir un type"
            assert isinstance(axiom["type"], str), "Le type d'axiom doit être une chaîne"
            
            # Vérification spécifique selon le type d'axiome
            if axiom["type"] == "subClassOf":
                assert set(axiom.keys()) == {"type", "subclass", "superclass"}
                assert all(isinstance(axiom[k], str) for k in ["subclass", "superclass"])
            
            elif axiom["type"] == "disjointClasses":
                assert set(axiom.keys()) == {"type", "classes"}
                assert isinstance(axiom["classes"], list)
                assert all(isinstance(c, str) for c in axiom["classes"])
            
            elif axiom["type"] == "equivalentClasses":
                assert set(axiom.keys()) == {"type", "classes"}
                assert isinstance(axiom["classes"], list)
                assert all(isinstance(c, str) for c in axiom["classes"])
            
            elif axiom["type"] == "cardinality":
                assert set(axiom.keys()) == {"type", "property", "domain", "cardinality"}
                assert isinstance(axiom["property"], str)
                assert isinstance(axiom["domain"], str)
                assert isinstance(axiom["cardinality"], dict)
                assert set(axiom["cardinality"].keys()) <= {"min", "max"}
                
            elif axiom["type"] == "functionalProperty":
                assert set(axiom.keys()) == {"type", "property"}
                assert isinstance(axiom["property"], str)
                
        # Vérification du contenu minimal attendu pour un système universitaire
        # assert len(result["classes"]) >= 3, "Devrait avoir au moins 3 classes (Student, Professor, Course)"
        # assert len(result["object_properties"]) >= 1, "Devrait avoir au moins une relation entre classes"
        # assert len(result["data_properties"]) >= 1, "Devrait avoir au moins une propriété de données"
