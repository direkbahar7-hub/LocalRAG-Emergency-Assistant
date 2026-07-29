print("EMBEDDING.PY YENİ SÜRÜM ÇALIŞTI")
from foundry_local_sdk import FoundryLocalManager

def load_embedding_model():
    manager = FoundryLocalManager.instance

    if manager is None:
        raise Exception("FoundryLocalManager initialize edilmemiş!")

    model = manager.catalog.get_model("qwen3-embedding-0.6b")

    if model is None:
        raise Exception("Embedding modeli bulunamadı!")

    if not model.is_cached:
        print("Embedding modeli indiriliyor...")
        model.download()

    model.load()

    embedding_client = model.get_embedding_client()

    print("Embedding client:", embedding_client)

    if embedding_client is None:
        raise Exception("Embedding Client oluşturulamadı!")

    return embedding_client


def create_embedding(embedding_client, text):
    response = embedding_client.generate_embedding(text)
    return response.data[0].embedding