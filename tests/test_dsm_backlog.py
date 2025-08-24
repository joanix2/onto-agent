
import pytest

from src.core.llms import get_completion

def test_get_completion(setup_environment):
    template_env, chatgpt = setup_environment
    system_data = {}
    user_data = {"prompt": "créer moi un modèle MVC"}
    # Appel de la fonction à tester
    result = get_completion(chatgpt, template_env, "dsm_backlog", system_data, user_data)
    # Vérification basique (à adapter selon le comportement attendu)
    assert isinstance(result, dict)