
import pytest

from src.core.llms import get_completion
from src.features.dsm_backlog.dsm_backlog_agent import generate_dsm_backlog

class TestOntoAgents:
    @pytest.fixture(autouse=True)
    def setup(self, setup_environment):
        """Configure l'environnement de test avec le modèle LLM"""
        self.model = setup_environment
        return self.model

    def test_get_completion(self):
        """Test que la fonction get_completion retourne une liste de chaînes"""
        prompt = "créer moi un modèle MVC"
        result = generate_dsm_backlog(self.model, prompt)
        # Vérification basique (à adapter selon le comportement attendu)
        print("result:", result)
        assert isinstance(result, list)
        assert len(result) > 0  # On s'attend à avoir au moins un élément
        assert all(isinstance(item, str) for item in result)  # Tous les éléments doivent être des strings