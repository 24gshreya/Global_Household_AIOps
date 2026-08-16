from sentence_transformers import (
    SentenceTransformer,
)


DEFAULT_EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


class EmbeddingModel:

    def __init__(
        self,
        model_name: str = DEFAULT_EMBEDDING_MODEL,
    ):
        self.model_name = model_name

        self.model = SentenceTransformer(
            model_name
        )

    def encode(
        self,
        texts: list[str],
    ):
        return self.model.encode(
            texts,
            normalize_embeddings=True,
        )