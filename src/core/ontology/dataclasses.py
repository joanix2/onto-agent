import pytest
from src.features.ontology_triplets.ontology_triplets_agent import generate_ontology_triplets

class TestOntologyTriplets:
    @pytest.fixture(autouse=True)
    def setup(self, setup_environment):
        """Configure l'environnement de test avec le modèle LLM"""
        self.model = setup_environment
        return self.model

    def test_generate_ontology_triplets(self):
        """Test la génération d'une ontologie (format MOF-like)"""
        # Données de test (backlog très simple)
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
        # On suppose que generate_ontology_triplets renvoie une liste de résultats ;
        # on teste le premier.
        result = generate_ontology_triplets(self.model, dms_backlog, lang="Français")[0]

        # ---- Structure racine ----
        assert isinstance(result, dict), "Le résultat doit être un dictionnaire"

        required_top_keys = {"entities", "relations", "constraints"}
        assert set(result.keys()) == required_top_keys, (
            f"Le résultat doit contenir exactement les clés {required_top_keys}"
        )

        # ---- entities ----
        entities = result["entities"]
        assert isinstance(entities, dict), "`entities` doit être un dictionnaire"
        assert set(entities.keys()) == {"classes", "individuals"}, \
            "`entities` doit contenir exactement `classes` et `individuals`"

        assert isinstance(entities["classes"], list), "`entities.classes` doit être une liste"
        assert all(isinstance(c, str) for c in entities["classes"]), \
            "Chaque classe doit être une chaîne"

        assert isinstance(entities["individuals"], list), "`entities.individuals` doit être une liste"
        assert all(isinstance(i, str) for i in entities["individuals"]), \
            "Chaque individu doit être une chaîne"

        # ---- relations ----
        relations = result["relations"]
        assert isinstance(relations, dict), "`relations` doit être un dictionnaire"
        assert set(relations.keys()) == {"object_properties", "data_properties"}, \
            "`relations` doit contenir exactement `object_properties` et `data_properties`"

        # object_properties
        assert isinstance(relations["object_properties"], list), "`object_properties` doit être une liste"
        for prop in relations["object_properties"]:
            assert isinstance(prop, dict), "Chaque object_property doit être un dictionnaire"
            assert set(prop.keys()) == {"name", "domain", "range"}, \
                "Chaque object_property doit avoir `name`, `domain`, `range`"
            assert all(isinstance(prop[k], str) for k in ["name", "domain", "range"]), \
                "Les champs `name`, `domain`, `range` doivent être des chaînes"

        # data_properties
        assert isinstance(relations["data_properties"], list), "`data_properties` doit être une liste"
        for prop in relations["data_properties"]:
            assert isinstance(prop, dict), "Chaque data_property doit être un dictionnaire"
            assert set(prop.keys()) == {"name", "domain", "range"}, \
                "Chaque data_property doit avoir `name`, `domain`, `range`"
            assert all(isinstance(prop[k], str) for k in ["name", "domain", "range"]), \
                "Les champs `name`, `domain`, `range` doivent être des chaînes"

        # ---- constraints ----
        constraints = result["constraints"]
        assert isinstance(constraints, dict), "`constraints` doit être un dictionnaire"

        expected_constraint_keys = {
            "subClassOf",
            "disjointClasses",
            "equivalentClasses",      # présent même si vide (ontologie fermée : tu peux décider de le laisser vide)
            "cardinality",
            "functionalProperty",
        }
        # Autoriser des sections vides, mais toutes les clés doivent exister
        assert set(constraints.keys()) == expected_constraint_keys, \
            f"`constraints` doit contenir exactement {expected_constraint_keys}"

        # subClassOf
        assert isinstance(constraints["subClassOf"], list), "`constraints.subClassOf` doit être une liste"
        for ax in constraints["subClassOf"]:
            assert isinstance(ax, dict), "Chaque entrée subClassOf doit être un dict"
            assert set(ax.keys()) == {"subclass", "superclass"}, \
                "subClassOf attend `subclass`, `superclass`"
            assert all(isinstance(ax[k], str) for k in ["subclass", "superclass"]), \
                "`subclass` et `superclass` doivent être des chaînes"

        # disjointClasses
        assert isinstance(constraints["disjointClasses"], list), "`constraints.disjointClasses` doit être une liste"
        for ax in constraints["disjointClasses"]:
            assert isinstance(ax, dict), "Chaque entrée disjointClasses doit être un dict"
            assert set(ax.keys()) == {"classes"}, "disjointClasses attend `classes`"
            assert isinstance(ax["classes"], list), "`classes` doit être une liste"
            assert all(isinstance(c, str) for c in ax["classes"]), "Chaque classe doit être une chaîne"
            assert len(ax["classes"]) >= 2, "disjointClasses doit contenir au moins 2 classes"

        # equivalentClasses (si tu gardes la clé mais que tu merges ensuite, elle peut être vide)
        assert isinstance(constraints["equivalentClasses"], list), "`constraints.equivalentClasses` doit être une liste"
        for ax in constraints["equivalentClasses"]:
            assert isinstance(ax, dict), "Chaque entrée equivalentClasses doit être un dict"
            assert set(ax.keys()) == {"classes"}, "equivalentClasses attend `classes`"
            assert isinstance(ax["classes"], list), "`classes` doit être une liste"
            assert all(isinstance(c, str) for c in ax["classes"]), "Chaque classe doit être une chaîne"
            assert len(ax["classes"]) == 2, "equivalentClasses attend exactement 2 classes"

        # cardinality
        assert isinstance(constraints["cardinality"], list), "`constraints.cardinality` doit être une liste"
        for ax in constraints["cardinality"]:
            assert isinstance(ax, dict), "Chaque entrée cardinality doit être un dict"
            assert set(ax.keys()) == {"property", "domain", "cardinality"}, \
                "cardinality attend `property`, `domain`, `cardinality`"
            assert isinstance(ax["property"], str) and isinstance(ax["domain"], str), \
                "`property` et `domain` doivent être des chaînes"
            assert isinstance(ax["cardinality"], dict), "`cardinality` doit être un dict"
            # clés optionnelles dans cardinality
            allowed_card_keys = {"min", "max", "exact"}
            assert set(ax["cardinality"].keys()) <= allowed_card_keys, \
                f"`cardinality` accepte uniquement {allowed_card_keys}"
            # types de valeurs : min/exact -> int|None ; max -> int|string|None
            if "min" in ax["cardinality"] and ax["cardinality"]["min"] is not None:
                assert isinstance(ax["cardinality"]["min"], int)
            if "exact" in ax["cardinality"] and ax["cardinality"]["exact"] is not None:
                assert isinstance(ax["cardinality"]["exact"], int)
            if "max" in ax["cardinality"] and ax["cardinality"]["max"] is not None:
                assert isinstance(ax["cardinality"]["max"], (int, str))

        # functionalProperty
        assert isinstance(constraints["functionalProperty"], list), "`constraints.functionalProperty` doit être une liste"
        for ax in constraints["functionalProperty"]:
            assert isinstance(ax, dict), "Chaque entrée functionalProperty doit être un dict"
            assert set(ax.keys()) == {"property"}, "functionalProperty attend `property`"
            assert isinstance(ax["property"], str), "`property` doit être une chaîne"
