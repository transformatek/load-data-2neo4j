import requests
import os
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

HF_TOKEN = os.getenv("WRITE_TOKEN")
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


class DynamicExample:

    def __init__(self):
        with open(
            os.path.join(os.path.dirname(__file__),
                         "../../data/embeddings/examples.json"), "r"
        ) as f:
            self.examples = json.load(f)
        with open(
            os.path.join(os.path.dirname(__file__),
                         "../../data/embeddings/embeddings.csv"), "r"
        ) as f:
            self.embeddings = pd.read_csv(f)

    def query(self, texts: list[str]):
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": texts, "options": {"wait_for_model": True}},
        )
        return response.json()

    def cosine_similarity(self, embedding_vector_a, embedding_vector_b):
        embedding_vector_a = np.array(embedding_vector_a)
        embedding_vector_b = np.array(embedding_vector_b)
        dot_product = np.dot(embedding_vector_a, embedding_vector_b)
        magnitude_a = np.linalg.norm(embedding_vector_a)
        magnitude_b = np.linalg.norm(embedding_vector_b)

        cosine_similarity = dot_product / (magnitude_a * magnitude_b)
        return cosine_similarity

    def get_k_most_similar(self, embeddings, target_embedding, top_k=5):
        embeddings = np.array(embeddings)
        target_embedding = np.array(target_embedding)

        similarities = np.array(
            [
                self.cosine_similarity(target_embedding, embedding)
                for embedding in embeddings
            ]
        )

        top_k_indices = np.argsort(similarities)[-top_k:][::-1]
        top_k_embeddings = embeddings[top_k_indices]
        return top_k_indices, top_k_embeddings, similarities[top_k_indices]

    def get_examples(self, user_input: list[str], top_k=5):
        embeddings = self.embeddings
        examples = self.examples
        dataset_embeddings = np.array(embeddings)
        question = self.query(user_input)
        query_embeddings = np.array(question)
        hits = self.get_k_most_similar(
            dataset_embeddings, query_embeddings, top_k)
        return [examples[index] for index in hits[0]]
