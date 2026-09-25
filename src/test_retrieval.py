from retriever import Retriever


def main():
    retriever = Retriever()

    query = "How can soil fertility be maintained?"

    print("\nQUERY:")
    print(query)

    results = retriever.search(query, top_k=5)

    print("\nRETRIEVED RESULTS:\n")

    for i, result in enumerate(results, start=1):
        print("=" * 80)
        print(f"RESULT {i}")
        print(f"Book: {result['title']}")
        print(f"Author: {result['author']}")
        print(f"Chunk: {result['chunk_id']}")
        print(f"Score: {result['score']:.4f}")
        print()
        print(result["text"][:1200])
        print()


if __name__ == "__main__":
    main()