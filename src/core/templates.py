
import json
from jinja2 import Environment, FileSystemLoader
from jinja2 import StrictUndefined, UndefinedError

def render_template(template_dir, template_file, json_data={}):
    """
    Charge un template Jinja depuis un dossier et le rend avec des données JSON.

    Args:
        template_dir (str): dossier contenant les templates (.txt, .j2, etc.)
        template_file (str): nom du fichier template
        json_data (dict | str): données JSON (dict Python ou string JSON)

    Returns:
        str: texte rendu avec les données injectées

    Raises:
        jinja2.exceptions.UndefinedError: si une variable du template est manquante dans json_data
    """

    # Si json_data est une string, on le parse en dict
    if isinstance(json_data, str):
        json_data = json.loads(json_data)

    # Créer un environnement Jinja2 avec le dossier des templates et StrictUndefined
    env = Environment(
        loader=FileSystemLoader(template_dir),
        undefined=StrictUndefined
    )

    # Charger le template
    template = env.get_template(template_file)

    try:
        # Rendre le template avec les données
        return template.render(json_data)
    except UndefinedError as e:
        raise ValueError(f"Une variable du template est manquante dans json_data: {e}")