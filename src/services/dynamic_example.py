import os
import json
import pandas as pd
import numpy as np
from utils.embedding_query import query


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

    def cosine_similarity(self, embedding_vector_a, embedding_vector_b):
        """
        Calculate the cosine similarity between two vectors.
        Args:
            embedding_vector_a (np.array): The first vector.
            embedding_vector_b (np.array): The second vector.
        Returns:
            float: The cosine similarity between the two vectors.
        """
        embedding_vector_a = np.array(embedding_vector_a)
        embedding_vector_b = np.array(embedding_vector_b)
        dot_product = np.dot(embedding_vector_a, embedding_vector_b)
        magnitude_a = np.linalg.norm(embedding_vector_a)
        magnitude_b = np.linalg.norm(embedding_vector_b)

        cosine_similarity = dot_product / (magnitude_a * magnitude_b)
        return cosine_similarity

    def get_k_most_similar(self, embeddings, target_embedding, top_k, threshold):
        """
        Get the k most similar embeddings to a target embedding.
        Args:
            embeddings (np.array): A list of embeddings.
            target_embedding (np.array): The target embedding.
            top_k (int): The number of most similar embeddings to return.
            threshold (float): The minimum similarity threshold.
        Returns:
            np.array: The indices of the k most similar embeddings.
            np.array: The k most similar embeddings.
            np.array: The cosine similarities of the k most similar embeddings.
        """
        embeddings = np.array(embeddings)
        target_embedding = np.array(target_embedding)

        similarities = np.array(
            [
                self.cosine_similarity(target_embedding, embedding)
                for embedding in embeddings
            ]
        )

        top_k_indices = np.argsort(similarities)[-top_k:][::-1]
        top_k_indices = top_k_indices[similarities[top_k_indices] >= threshold]
        top_k_embeddings = embeddings[top_k_indices]
        return top_k_indices, top_k_embeddings, similarities[top_k_indices]

    def get_examples(self, user_input: list[str], top_k=5, threshold=0.6):
        """
        Get the most similar examples to a user input.
        Args:
            user_input (list[str]): The user input.
            top_k (int): The number of most similar examples to return.
            threshold (float): The minimum similarity threshold.
        Returns:
            list: The most similar examples to the user input.
        """
        embeddings = self.embeddings
        examples = self.examples
        dataset_embeddings = np.array(embeddings)
        question = query(user_input)
        query_embeddings = np.array(question)
        hits = self.get_k_most_similar(
            dataset_embeddings, query_embeddings, top_k, threshold
        )
        return [
            {"input": example, "embedding": embedding, "similarity": similarity}
            for example, embedding, similarity in zip(
                [examples[index]["input"]
                    for index in hits[0]], hits[1], hits[2]
            )
        ]
