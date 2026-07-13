import json
import numpy as np

embeddings = np.load("../dataset/embeddings/pokemon_embeddings.npy")

with open("../dataset/embeddings/card_names.json", encoding="utf8") as f:
    nombres = json.load(f)

with open("../dataset/embeddings/processed_index.json", encoding="utf8") as f:
    indice = json.load(f)

print(f"Embeddings: {embeddings.shape}")
print(f"Nombres: {len(nombres)}")
print(f"Índice: {len(indice)}")

if embeddings.shape[0] == len(nombres) == len(indice):
    print("✅ Todo está sincronizado.")
else:
    print("❌ Hay diferencias entre los archivos.")