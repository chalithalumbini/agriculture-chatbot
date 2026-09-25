import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


INDEX_FILE = Path("vectorstore/books.faiss")
METADATA_FILE = Path("vectorstore/metadata.pkl")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class Retriever:

    def __init__(self):
        print("Loading FAISS index...")
        self.index = faiss.read_index(str(INDEX_FILE))

        print("Loading metadata...")
        with open(METADATA_FILE, "rb") as f:
            self.metadata = pickle.load(f)

        print("Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)

    def search(self, query, top_k=5):
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        query_embedding = query_embedding.astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            result = self.metadata[index].copy()
            result["score"] = float(score)

            results.append(result)

        return results
