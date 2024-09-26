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
        """
        Retrieve search hits based on the provided embedding.
        Args:
            embedding (list or numpy.ndarray): The embedding vector to search for.
        Returns:
            list: A list of search hits retrieved from the Qdrant service.
        """

        qdrant = self.qdrant_service
        hits = qdrant.search('document', embedding)
        return hits

    def similar(self, embedding):
        """
        Finds and returns sentences similar to the given embedding.
        Args:
            embedding (list or np.ndarray): The embedding vector to find similar sentences for.
        Returns:
            str: A newline-separated string of sentences similar to the given embedding.
        """

        hits = self.get_hits(embedding)
        return '\n'.join([hit.payload['sentence'] for hit in hits])

    def get_summary(self):
        """
        Generates a summary of the document based on its embedding.
        This method performs the following steps:
        1. Retrieves the document embedding.
        2. Finds similar documents based on the embedding.
        3. Constructs a prompt with the similar documents.
        4. Uses an AI model service to generate a summary from the prompt.
        Returns:
            str: The generated summary of the document.
        """
        embedding = self.document_embedding
        similar = self.similar(embedding)
        print(similar)
        ai_model = self.ai_model_service()
        prompt = f"""Generate a summary of the following sentences: 
        {similar}
        """
        return ai_model(prompt)
