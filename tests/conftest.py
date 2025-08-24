import pytest
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from jinja2 import Environment, FileSystemLoader

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    # Charger les variables d'environnement depuis .env
    load_dotenv()
    # Activer le cache SQLite pour LangChain
    set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))

    chatgpt = ChatOpenAI(model="gpt-4",temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    return chatgpt