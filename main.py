from foundry_local_sdk import Configuration, FoundryLocalManager
from src.pdf_loader import load_all_pdfs
from src.text_splitter import split_text
from src.embedding import load_embedding_model, create_embedding

print("Foundry Local başlatılıyor...")

config = Configuration(app_name="OfflineEmergencyAssistant")
FoundryLocalManager.initialize(config)

manager = FoundryLocalManager.instance

print("Execution providers hazırlanıyor...")
manager.download_and_register_eps()

print("\nKatalogdaki modeller:\n")

for model in manager.catalog.list_models():
    print(model.id)

print("Model seçiliyor...")

model = manager.catalog.get_model("phi-3.5-mini")

print("Model bulundu.")

if not model.is_cached:
    print("Model indiriliyor...")
    model.download()

model.load()

print("Model yüklendi!")
print("Model ID:", model.id)
print("Cached:", model.is_cached)

print("Sohbet istemcisi oluşturuluyor...")

client = model.get_chat_client()

print("Sohbet istemcisi hazır!")

messages = [
    {
        "role": "user",
        "content": "Merhaba! Sen kimsin?"
    }
]

response = client.complete_chat(messages)

print("\nModelin cevabı:\n")
print(response.choices[0].message.content)

print("\nPDF'ler okunuyor...")

documents = load_all_pdfs("documents")

print(f"\nToplam {len(documents)} PDF okundu.")

print("\nİlk PDF:")
print(documents[0]["file_name"])

print("\nİlk 1000 karakter:\n")
print(documents[0]["text"][:1000])

print("\nChunk'lar oluşturuluyor...")

all_chunks = []

for document in documents:
    chunks = split_text(document["text"])

    for chunk in chunks:
        all_chunks.append({
            "file_name": document["file_name"],
            "text": chunk
        })

print(f"Toplam Chunk Sayısı: {len(all_chunks)}")

print("\nİlk Chunk:\n")
print(all_chunks[0]["text"])

print("\nEmbedding modeli yükleniyor...")

embedding_client = load_embedding_model()

print("\nTüm chunk'lar için embedding oluşturuluyor...")

embedded_chunks = []

total = len(all_chunks)

for i, chunk in enumerate(all_chunks, start=1):
    response = embedding_client.generate_embedding(chunk["text"])

    vector = response.data[0].embedding

    embedded_chunks.append({
        "file_name": chunk["file_name"],
        "text": chunk["text"],
        "embedding": vector
    })

    print(f"[{i}/{total}] tamamlandı")

print("\nToplam embedding sayısı:", len(embedded_chunks))
print("\nİlk embedding boyutu:", len(embedded_chunks[0]["embedding"]))
  