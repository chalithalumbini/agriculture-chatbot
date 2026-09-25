import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


CHUNKS_FILE = Path("data/chunks.json")
VECTORSTORE_DIR = Path("vectorstore")

INDEX_FILE = VECTORSTORE_DIR / "books.faiss"
METADATA_FILE = VECTORSTORE_DIR / "metadata.pkl"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading chunks...")

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Number of chunks: {len(chunks)}")

    texts = [chunk["text"] for chunk in chunks]

    print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    print("Creating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    print(f"Embedding shape: {embeddings.shape}")

    # Because embeddings are normalized,
    # inner product is equivalent to cosine similarity.
    dimension = embeddings.shape[1]

    print(f"Creating FAISS index with dimension {dimension}...")

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    print(f"FAISS index contains {index.ntotal} vectors")

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    with open(METADATA_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print(f"Saved FAISS index: {INDEX_FILE}")
    print(f"Saved metadata: {METADATA_FILE}")


if __name__ == "__main__":
    main()