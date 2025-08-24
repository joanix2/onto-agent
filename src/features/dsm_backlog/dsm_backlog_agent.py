
from src.core.llms import get_completion

def generate_dsm_backlog(model, prompt):
    user_data = {"prompt": prompt}

    # Appel de la fonction à tester
    return get_completion(model, "dsm_backlog", user_data=user_data)