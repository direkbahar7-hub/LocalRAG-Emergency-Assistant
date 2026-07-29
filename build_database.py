from src.pdf_loader import load_all_pdfs
from src.database import create_database, insert_chunks
from src.embedding import load_embedding_model, create_embedding
from foundry_local_sdk import Configuration, FoundryLocalManager

PDF_FOLDER = "documents"


def main():

    config = Configuration(app_name="OfflineEmergencyAssistant")
    FoundryLocalManager.initialize(config)

    manager = FoundryLocalManager.instance
    manager.download_and_register_eps()

    print("SQLite oluşturuluyor...")
    create_database()

    print("PDF'ler okunuyor...")
    documents = load_all_pdfs(PDF_FOLDER)

    print(f"{len(documents)} sayfa bulundu.\n")

    # TEST
    print("\n========== İLK SAYFA ==========\n")
    print(documents[0]["text"])
    print("\n===============================\n")

    embedding_client = load_embedding_model()

    chunks = []

    for index, doc in enumerate(documents, start=1):

        print(
            f"[{index}/{len(documents)}] Embedding oluşturuluyor -> "
            f"{doc['file_name']} | Sayfa {doc['page']}"
        )

        embedding = create_embedding(
            embedding_client,
            doc["text"]
        )

        chunks.append({
            "file_name": doc["file_name"],
            "text": doc["text"],
            "embedding": embedding
        })

    print("\nVeritabanına kaydediliyor...")
    insert_chunks(chunks)

    print("\n✅ Veritabanı başarıyla oluşturuldu.")
    print(f"Toplam chunk: {len(chunks)}")


if __name__ == "__main__":
    main()