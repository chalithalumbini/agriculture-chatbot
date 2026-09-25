from pathlib import Path
import re

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_gutenberg_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # ---------------------------------------------------------
    # Remove everything before the Gutenberg START marker
    # ---------------------------------------------------------
    start = re.search(
        r"\*\*\*\s*START OF (?:THE )?PROJECT GUTENBERG EBOOK.*?\*\*\*",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if start:
        text = text[start.end():]
    else:
        print("WARNING: START marker not found")

    # ---------------------------------------------------------
    # Remove Gutenberg credits after START
    # ---------------------------------------------------------
    # These credits are not part of the book.
    credit_patterns = [
        r"Produced by .*?Distributed Proofreading Team.*?\n",
        r"This file is gratefully uploaded.*?10,000 ebooks\.\s*",
    ]

    for pattern in credit_patterns:
        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

    # ---------------------------------------------------------
    # Remove Gutenberg END marker and everything after it
    # ---------------------------------------------------------
    end = re.search(
        r"\*\*\*\s*END OF (?:THE )?PROJECT GUTENBERG EBOOK.*",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if end:
        text = text[:end.start()]

    # ---------------------------------------------------------
    # Clean whitespace while preserving paragraphs
    # ---------------------------------------------------------
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def process_book(path: Path):
    print(f"Processing {path.name}")

    text = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    cleaned = clean_gutenberg_text(text)

    output_path = PROCESSED_DIR / path.name

    output_path.write_text(
        cleaned,
        encoding="utf-8",
    )

    print(f"Saved: {output_path}")


def main():
    files = sorted(RAW_DIR.glob("*.txt"))

    print(f"Found {len(files)} raw books")

    for path in files:
        process_book(path)


if __name__ == "__main__":
    main()
