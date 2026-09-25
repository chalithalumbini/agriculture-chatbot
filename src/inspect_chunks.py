import json

with open("data/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

print("Total chunks:", len(chunks))

print("\nFirst 10 chunk IDs:")
for chunk in chunks[:10]:
    print(chunk["chunk_id"], "-", chunk["title"])

print("\n--- CHUNK 1 ---")
print(chunks[1]["text"][:1000])

print("\n--- CHUNK 30 ---")
print(chunks[30]["text"][:1000])