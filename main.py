import json
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.features.ontology_triplets.ontology_triplets_agent import generate_ontology_triplets
import os


def main():
    # Charger les variables d'environnement depuis .env
    load_dotenv()
    # Activer le cache SQLite pour LangChain
    set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))

    model = ChatOpenAI(model="gpt-4",temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

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
    results = generate_ontology_triplets(model, dms_backlog, lang="Français")

    for log, result in zip(dms_backlog,results):
        print(f"{log}:\n{json.dumps(result, ensure_ascii=False, indent=2)}")

if __name__ == "__main__":
    main()