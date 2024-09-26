from services.ai_model_service import AIModelService
from services.qdrant_service import QdrantService
from services.document_service import Document
from utils.embedding_query import query


class VDBPrompt:

    def __init__(self, text: str):
        self.ai_model_service = AIModelService()
        qdrant = self.qdrant_service = QdrantService()
        doc = self.document = Document(text)
        self.document_embedding = query([text])
        qdrant.create_collection("document")
        embeddings = doc.load_embeddings()
        qdrant.insert_vectors("document", embeddings)

    def get_hits(self, embedding):
        qdrant = self.qdrant_service
        hits = qdrant.search('document', embedding)
        return hits

    def similar(self, embedding):
        hits = self.get_hits(embedding)
        return '\n'.join([hit.payload['sentence'] for hit in hits])

    def get_summary(self):
        embedding = self.document_embedding
        similar = self.similar(embedding)
        print(similar)
        ai_model = self.ai_model_service()
        prompt = f"""Generate a summary of the following sentences: 
        {similar}
        """
        return ai_model(prompt)
