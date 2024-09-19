import requests
import os
import torch
import json
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from sentence_transformers.util import semantic_search

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

HF_TOKEN = os.getenv("WRITE_TOKEN")
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


class DynamicExample:

    def query(self, texts: list[str]):
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": texts, "options": {"wait_for_model": True}},
        )
        return response.json()

    def get_examples(self, user_input: list[str], top_k=5):
        with open(
            os.path.join(os.path.dirname(__file__),
                         "../../data/embeddings/examples.json"), "r"
        ) as f:
            examples = json.load(f)
        with open(
            os.path.join(os.path.dirname(__file__),
                         "../../data/embeddings/embeddings.csv"), "r"
        ) as f:
            embeddings = pd.read_csv(f)
        dataset_embeddings = torch.from_numpy(
            embeddings.to_numpy()).to(torch.float)
        question = self.query(user_input)
        query_embeddings = torch.FloatTensor(question)
        hits = semantic_search(
            query_embeddings, dataset_embeddings, top_k=top_k)
        return [examples[hit["corpus_id"]]["query"] for hit in hits[0]]
