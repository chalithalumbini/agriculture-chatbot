from pathlib import Path
import json


PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = Path("data/chunks.json")


MAX_CHARS = 4000
OVERLAP_CHARS = 500


BOOK_METADATA = {
    "56640": {
        "title": "Pleasant Talk About Fruits, Flowers and Farming",
        "author": "Henry Ward Beecher",
    },
    "67813": {
        "title": "Field, Forest and Farm",
        "author": "Jean-Henri Fabre",
    },
    "20772": {
        "title": "Agriculture for Beginners",
        "author": "Charles William Burkett, Frank Lincoln Stevens, Daniel Harvey Hill",
    },
    "40190": {
        "title": "Science and Practice in Farm Cultivation",
        "author": "James Buckman",
    },
    "4924": {
        "title": "Dry-Farming",
        "author": "John Andreas Widtsoe",
    },
    "4525": {
        "title": "The Farm That Won't Wear Out",
        "author": "Cyril G. Hopkins",
    },
}


def create_chunks(text, max_chars=MAX_CHARS, overlap=OVERLAP_CHARS):

    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:

        candidate = (
            f"{current}\n\n{paragraph}"
            if current
            else paragraph
        )

        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)

            overlap_text = current[-overlap:] if current else ""
            current = f"{overlap_text}\n\n{paragraph}".strip()

    if current:
        chunks.append(current)

    return chunks


def main():

    all_chunks = []

    for path in PROCESSED_DIR.glob("*.txt"):

        book_id = path.stem
        text = path.read_text(encoding="utf-8")

        chunks = create_chunks(text)

        metadata = BOOK_METADATA.get(book_id, {})

        for i, chunk in enumerate(chunks):

            all_chunks.append(
                {
                    "chunk_id": f"{book_id}_{i}",
                    "book_id": book_id,
                    "title": metadata.get("title", ""),
                    "author": metadata.get("author", ""),
                    "chunk_index": i,
                    "text": chunk,
                }
            )

        print(f"{book_id}: {len(chunks)} chunks")

    OUTPUT_FILE.write_text(
        json.dumps(all_chunks, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
