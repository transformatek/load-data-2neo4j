from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


class QdrantService:
    def __init__(self):
        self.client = QdrantClient(url="http://vdb:6333")

    def __call__(self):
        return self.client

    def create_collection(self, collection_name: str):
        if not self().collection_exists(collection_name):
            self().create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

    def insert_vectors(self, collection_name: str, vectors):
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
        points = self.client.scroll(
            collection_name=collection_name, limit=1000)

        ids = [point.id for point in points]

        if len(ids) > 0:
            self.client.delete(
                collection_name=collection_name, points=ids)

    def search(self, collection_name, target_vector, top_k=5):
        hits = self().search(
            collection_name=collection_name,
            query_vector=target_vector,
            limit=top_k
        )
        return hits
