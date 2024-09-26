import re
from utils.embedding_query import query


class Document:
    def __init__(self, text: str, chunk_size=1):
        sentences = re.split(r"(?<=[.!?]) +", text)

        chunks = [
            " ".join(sentences[i: i + chunk_size])
            for i in range(0, len(sentences), chunk_size)
        ]
        self.chunks = chunks

    def load_embeddings(self):
        """
        Load the embeddings for each chunk of the document.
        Returns:
            list: The embeddings for the document.
        """
        return [(query(chunk), chunk) for chunk in self.chunks]
