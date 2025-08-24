
import json

def render_template(env, template_file, json_data={}):
    """
    Charge un template Jinja depuis un dossier et le rend avec des données JSON.
    
    Args:
        template_dir (str): dossier contenant les templates (.txt, .j2, etc.)
        template_file (str): nom du fichier template
        json_data (dict | str): données JSON (dict Python ou string JSON)
    
    Returns:
        str: texte rendu avec les données injectées
    """
    # Si json_data est une string, on le parse en dict
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    
    # Charger le template
    template = env.get_template(template_file)
    
    # Rendre le template avec les données
    return template.render(json_data)