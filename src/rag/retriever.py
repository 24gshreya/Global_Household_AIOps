from src.rag.chunking import chunk_text
from src.rag.embeddings import EmbeddingModel
from src.rag.ingest import (
    load_knowledge_documents,
)
from src.rag.vector_store import VectorStore


class HouseholdRetriever:

    def __init__(
        self,
        knowledge_dir: str = "knowledge",
    ):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

        documents = load_knowledge_documents(
            knowledge_dir
        )

        chunks = []

        for document in documents:

            for chunk in chunk_text(
                document["text"]
            ):
                chunks.append(
                    {
                        "source": document["source"],
                        "text": chunk,
                    }
                )

        embeddings = (
            self.embedding_model.encode(
                [
                    item["text"]
                    for item in chunks
                ]
            )
        )

        self.vector_store.build(
            embeddings,
            chunks,
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
    ) -> list[dict]:

        query_embedding = (
            self.embedding_model.encode(
                [query]
            )[0]
        )

        return self.vector_store.search(
            query_embedding,
            top_k=top_k,
        )
        