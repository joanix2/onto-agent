import copy
import pytest
from src.core.ontology.merge import merge_jsons

def test_merge_scalars_and_dicts_recursive():
    """Test la fusion récursive des dictionnaires"""
    a = {"a": 1, "b": {"x": 1, "y": 2}}
    b = {"a": 2, "b": {"y": 3, "z": 4}}
    merged = merge_jsons([a, b])
    assert merged == {"a": 2, "b": {"x": 1, "y": 3, "z": 4}}

def test_merge_lists_union_of_scalars():
    """Test l'union des listes de valeurs scalaires"""
    a = {"lst": [1, 2, 3]}
    b = {"lst": [3, 4]}
    c = {"lst": [4, 5, 5]}
    merged = merge_jsons([a, b, c])
    # ordre pas garanti, on compare en tant qu'ensemble
    assert set(merged["lst"]) == {1, 2, 3, 4, 5}

def test_merge_ontologies():
    """Test la fusion de plusieurs ontologies"""
    # Préparation des données de test
    json1 = {
        "entities": {
            "classes": ["Model", "View"],
            "individuals": ["instance1"]
        },
        "relations": {
            "object_properties": [
                {"name": "displays", "domain": "View", "range": "Model"}
            ],
            "data_properties": [
                {"name": "id", "domain": "Model", "range": "int"}
            ]
        },
        "constraints": {
            "subClassOf": [],
            "disjointClasses": [],
            "equivalentClasses": [],
            "cardinality": [],
            "functionalProperty": []
        }
    }

    json2 = {
        "entities": {
            "classes": ["Controller", "View"],
            "individuals": ["instance2"]
        },
        "relations": {
            "object_properties": [
                {"name": "updates", "domain": "Controller", "range": "Model"}
            ],
            "data_properties": [
                {"name": "name", "domain": "Model", "range": "string"}
            ]
        },
        "constraints": {
            "subClassOf": [],
            "disjointClasses": [{"classes": ["Model", "View"]}],
            "equivalentClasses": [],
            "cardinality": [
                {
                    "property": "updates",
                    "domain": "Controller",
                    "cardinality": {"min": 1, "max": 1}
                }
            ],
            "functionalProperty": []
        }
    }

    # Exécution de la fonction
    result = merge_jsons([json1, json2])

    # Vérifications
    assert isinstance(result, dict), "Le résultat doit être un dictionnaire"
    
    # Vérification des classes (union sans doublons)
    expected_classes = {"Model", "View", "Controller"}
    assert set(result["entities"]["classes"]) == expected_classes
    
    # Vérification des individuals (union sans doublons)
    expected_individuals = {"instance1", "instance2"}
    assert set(result["entities"]["individuals"]) == expected_individuals
    
    # Vérification des object_properties (union)
    assert len(result["relations"]["object_properties"]) == 2
    assert any(p["name"] == "displays" for p in result["relations"]["object_properties"])
    assert any(p["name"] == "updates" for p in result["relations"]["object_properties"])
    
    # Vérification des data_properties (union)
    assert len(result["relations"]["data_properties"]) == 2
    assert any(p["name"] == "id" for p in result["relations"]["data_properties"])
    assert any(p["name"] == "name" for p in result["relations"]["data_properties"])
    
    # Vérification des contraintes (fusion)
    assert len(result["constraints"]["disjointClasses"]) == 1
    assert len(result["constraints"]["cardinality"]) == 1
    assert result["constraints"]["cardinality"][0]["property"] == "updates"

def test_merge_ontologies_empty():
    """Test la fusion avec des ontologies vides"""
    json1 = {
        "entities": {
            "classes": [],
            "individuals": []
        },
        "relations": {
            "object_properties": [],
            "data_properties": []
        },
        "constraints": {
            "subClassOf": [],
            "disjointClasses": [],
            "equivalentClasses": [],
            "cardinality": [],
            "functionalProperty": []
        }
    }

    json2 = {
        "entities": {
            "classes": ["Model"],
            "individuals": []
        },
        "relations": {
            "object_properties": [],
            "data_properties": []
        },
        "constraints": {
            "subClassOf": [],
            "disjointClasses": [],
            "equivalentClasses": [],
            "cardinality": [],
            "functionalProperty": []
        }
    }

    result = merge_jsons([json1, json2])
    assert len(result["entities"]["classes"]) == 1
    assert result["entities"]["classes"][0] == "Model"

def test_merge_ontologies_duplicates():
    """Test la déduplication lors de la fusion d'ontologies"""
    json1 = {
        "entities": {
            "classes": ["Model", "View", "Model"],
            "individuals": ["instance1", "instance1"]
        },
        "relations": {
            "object_properties": [
                {"name": "displays", "domain": "View", "range": "Model"},
                {"name": "displays", "domain": "View", "range": "Model"}
            ],
            "data_properties": []
        },
        "constraints": {
            "subClassOf": [],
            "disjointClasses": [],
            "equivalentClasses": [],
            "cardinality": [],
            "functionalProperty": []
        }
    }

    json2 = {
        "entities": {
            "classes": ["Model", "Controller"],
            "individuals": ["instance1"]
        },
        "relations": {
            "object_properties": [
                {"name": "displays", "domain": "View", "range": "Model"}
            ],
            "data_properties": []
        },
        "constraints": {
            "subClassOf": [],
            "disjointClasses": [],
            "equivalentClasses": [],
            "cardinality": [],
            "functionalProperty": []
        }
    }

    result = merge_jsons([json1, json2])
    
    # Vérification de la déduplication
    assert len(result["entities"]["classes"]) == 3
    assert len(result["entities"]["individuals"]) == 1
    assert len(result["relations"]["object_properties"]) == 1

def test_merge_lists_union_of_dicts_dedup():
    a = {"items": [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}]}
    b = {"items": [{"id": 2, "v": "b"}, {"id": 3, "v": "c"}]}
    merged = merge_jsons([a, b])
    # déduplication logique attendue
    assert len(merged["items"]) == 3
    assert {"id": 1, "v": "a"} in merged["items"]
    assert {"id": 2, "v": "b"} in merged["items"]
    assert {"id": 3, "v": "c"} in merged["items"]

def test_deep_nested_merge_and_union():
    a = {"root": {"entities": {"classes": ["User"], "individuals": ["u1"]}}}
    b = {"root": {"entities": {"classes": ["Role"], "individuals": ["u2"]}}}
    c = {"root": {"relations": {"object_properties": [
        {"name": "hasRole", "domain": "User", "range": "Role"}
    ]}}}
    d = {"root": {"relations": {"object_properties": [
        {"name": "hasRole", "domain": "User", "range": "Role"}  # doublon exact
    ]}}}
    merged = merge_jsons([a, b, c, d])
    assert set(merged["root"]["entities"]["classes"]) == {"User", "Role"}
    assert set(merged["root"]["entities"]["individuals"]) == {"u1", "u2"}
    assert merged["root"]["relations"]["object_properties"] == [
        {"name": "hasRole", "domain": "User", "range": "Role"}
    ]

def test_inputs_are_not_mutated():
    original = {"lst": [1, 2], "obj": {"k": "v"}}
    a = copy.deepcopy(original)
    b = {"lst": [2, 3], "obj": {"k2": "v2"}}
    _ = merge_jsons([a, b])
    assert a == original, "Les entrées ne doivent pas être modifiées par la fusion"

def test_empty_and_none_values_are_ignored():
    a = {"x": None, "y": [], "z": {}}
    b = {"x": 1, "y": [1], "z": {"k": "v"}}
    merged = merge_jsons([a, b])
    assert merged["x"] == 1
    assert merged["y"] == [1]
    assert merged["z"] == {"k": "v"}

@pytest.mark.parametrize("inputs,expected", [
    # Aucun JSON
    ([], {}),
    # Un seul JSON
    ([{"a": 1}], {"a": 1}),
    # Conflit scalaire : dernière valeur l’emporte
    ([{"a": 1}, {"a": 2}], {"a": 2}),
])
def test_various_sanity_cases(inputs, expected):
    assert merge_jsons(inputs) == expected
