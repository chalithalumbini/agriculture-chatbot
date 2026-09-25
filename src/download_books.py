from pathlib import Path
import requests


BOOKS = {
    "56640": "Pleasant Talk About Fruits, Flowers and Farming",
    "67813": "Field, Forest and Farm",
    "20772": "Agriculture for Beginners",
    "40190": "Science and Practice in Farm Cultivation",
    "4924": "Dry-Farming",
    "4525": "The Farm That Won't Wear Out",
}


RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_book(book_id: str, title: str):
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"

    print(f"Downloading: {book_id} - {title}")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    output_file = RAW_DIR / f"{book_id}.txt"
    output_file.write_text(response.text, encoding="utf-8")

    print(f"Saved: {output_file}")


def main():
    for book_id, title in BOOKS.items():
        try:
            download_book(book_id, title)
        except Exception as exc:
            print(f"ERROR downloading {book_id}: {exc}")


if __name__ == "__main__":
    main()