from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


class QdrantService:
    def __init__(self):
        self.client = QdrantClient(url="http://vdb:6333")

    def __call__(self):
        return self.client

    def create_collection(self, collection_name: str):
        """
        Creates a new collection in the Qdrant service if it does not already exist.
        Args:
            collection_name (str): The name of the collection to be created.
        Returns:
            None
        """
        if not self().collection_exists(collection_name):
            self().create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

    def insert_vectors(self, collection_name: str, vectors):
        """
        Inserts vectors into a specified collection.
        Args:
            collection_name (str): The name of the collection to insert vectors into.
            vectors (list): A list of vectors to insert into the collection.
        Returns:
            None
        """
        self().upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=idx,
                    vector=vector[0],
                    payload={'sentence': vector[1]}
                )
                for idx, vector in enumerate(vectors)
            ]
        )

    def clear_collection(self, collection_name: str):
        """
        Clears all vectors from a specified collection.
        Args:
            collection_name (str): The name of the collection to clear.
        Returns:
            None
        """
        points = self.client.scroll(
            collection_name=collection_name, limit=1000)

        ids = [point.id for point in points]

        if len(ids) > 0:
            self.client.delete(
                collection_name=collection_name, points=ids)

    def search(self, collection_name, target_vector, top_k=5):
        """
        Searches for the most similar vectors in a collection to a target vector using cosine similarity.
        Args:
            collection_name (str): The name of the collection to search.
            target_vector (list): The target vector to compare against.
            top_k (int): The number of most similar vectors to return.
        Returns:
            list: A list of the most similar vectors to the target vector.
        """
        hits = self().search(
            collection_name=collection_name,
            query_vector=target_vector,
            limit=top_k
        )
        return hits
