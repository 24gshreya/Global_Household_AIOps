import faiss
import numpy as np


class VectorStore:

    def __init__(self):
        self.index = None
        self.documents = []

    def build(
        self,
        embeddings,
        documents,
    ) -> None:

        vectors = np.asarray(
            embeddings,
            dtype="float32",
        )

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(vectors)

        self.documents = documents

    def search(
        self,
        query_embedding,
        top_k: int = 4,
    ) -> list[dict]:

        vector = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        scores, indices = self.index.search(
            vector,
            top_k,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index == -1:
                continue

            result = dict(
                self.documents[index]
            )

            result["score"] = float(score)

            results.append(result)

        return results