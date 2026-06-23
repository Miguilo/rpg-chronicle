from openai import OpenAI, Client
import os
from functools import lru_cache
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

@lru_cache(maxsize=1)
def get_openai_client() -> Client:
    openai_key = os.environ.get("OPENAI_API_KEY")

    return OpenAI(api_key=openai_key)