import json
from src.core.templates import render_template

def llm_completion(model, system_prompt, user_prompt, as_json=True):
    """
    Interroge un LLM avec un prompt système et un prompt utilisateur.
    
    Args:
        model: instance du modèle (ex: chatgpt)
        system_prompt (str): prompt système
        user_prompt (str): prompt utilisateur
        as_json (bool): si True, tente de parser la réponse en JSON
    
    Returns:
        dict | str: dictionnaire si as_json=True, sinon texte brut
    """
    response = model.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])

    output = response.content.strip()
    
    if as_json:
        try:
            return json.loads(output)
        except Exception as e:
            raise RuntimeError(f"JSON parsing failed: {e}\n---\nRaw output:\n{output}")
    else:
        return output

def get_completion(model, template_env, templates_dir, system_data, user_data):
    
    sys_prompt_template = f"{templates_dir}/system.j2"
    user_prompt_template = f"{templates_dir}/user.j2"

    sys_prompt = render_template(template_env, sys_prompt_template, system_data)
    user_prompt = render_template(template_env, user_prompt_template, user_data)

    return llm_completion(model, sys_prompt, user_prompt)