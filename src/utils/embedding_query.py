import os
import requests
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

HF_TOKEN = os.getenv("WRITE_TOKEN")
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


def query(texts: list[str]):
    """
    Queries the Hugging Face API for text embeddings.
    Args:
        texts (list): A list of strings to embed.
    Returns:
        dict: The embeddings for the input texts.
    """
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": texts, "options": {"wait_for_model": True}},
    )
    return response.json()
