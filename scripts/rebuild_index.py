import json
from pathlib import Path

EMBEDDINGS = Path("../dataset/embeddings")

with open(EMBEDDINGS / "card_names.json", encoding="utf8") as f:
    nombres = json.load(f)

with open(EMBEDDINGS / "processed_index.json", "w", encoding="utf8") as f:
    json.dump(sorted(nombres), f, indent=4)

print(f"Índice reconstruido con {len(nombres)} cartas.")