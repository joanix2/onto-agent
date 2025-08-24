

from src.core.llms import get_completion


def generate_ontology_triplets(model, dms_backlog, lang = "Français"):
    sys_prompt_json_data = {
        "lang": lang,
    }

    print("dms_backlog:", dms_backlog)

    return [get_completion(model, "triplets", system_data=sys_prompt_json_data, user_data={"log": log}) for log in dms_backlog]