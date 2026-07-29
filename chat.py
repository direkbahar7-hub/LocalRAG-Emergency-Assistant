from foundry_local_sdk import Configuration, FoundryLocalManager
from src.retriever import search_chunks

print("🚀 Offline Emergency Assistant başlatılıyor...")

# Foundry Local başlat
config = Configuration(app_name="OfflineEmergencyAssistant")
FoundryLocalManager.initialize(config)

manager = FoundryLocalManager.instance
manager.download_and_register_eps()

# Chat modeli
model = manager.catalog.get_model("phi-3.5-mini")

if not model.is_cached:
    print("Model indiriliyor...")
    model.download()

model.load()

client = model.get_chat_client()

print("✅ Sistem hazır.")

while True:

    question = input("\nSorunuz (Çıkmak için 'çık'): ")

    if not question.strip():
        continue

    if question.lower() == "çık":
        print("\nProgram kapatılıyor...")
        break

    allowed_files = None
    q = question.lower()

    if "deprem" in q:
        allowed_files = ["afad_deprem_icin_hazirlik_rehberi.pdf"]

    elif "yangın" in q or "yangin" in q:
        allowed_files = ["afad_yangin_icin_hazirlik_rehberi.pdf"]

    elif "sel" in q:
        allowed_files = ["afad_sel_icin_hazirlik_rehberi.pdf"]

    elif "heyelan" in q:
        allowed_files = ["afad_heyelan_icin_hazirlik_rehberi.pdf"]

    elif "çığ" in q or "cig" in q:
        allowed_files = ["afad_cig_icin_hazirlik_rehberi.pdf"]

    results = search_chunks(question, allowed_files)

    if len(results) == 0:
        print("\n🤖 Asistanın Cevabı:\n")
        print("Bu soru, sağlanan resmi kaynaklarda cevaplanamamaktadır.")
        continue

    # Context oluştur
    unique_chunks = set()
    context_parts = []

    for result in results:

        text = result["chunk_text"].strip()

        if text in unique_chunks:
            continue

        unique_chunks.add(text)

        context_parts.append(
            f"Kaynak: {result['file_name']}\n{text}"
        )

    context = "\n\n".join(context_parts)

    print("Context uzunluğu:", len(context))
    messages = [
        {
            "role": "system",
            "content": """
 Sen AFAD ve MEB resmi dokümanlarını kullanan bir Acil Durum Asistanısın.

 Kurallar:

 1. Sadece verilen resmi kaynakları kullan.
 2. Kendi bilgini ASLA kullanma.
 3. Tahmin yürütme.
 4. Kaynakta olmayan hiçbir bilgiyi ekleme.
 5. Soruyla ilgili olan bilgileri kullan.
 6. Cevabı en fazla 3 madde halinde ver.
 7. Eğer cevap kaynaklarda açıkça yoksa SADECE şu cümleyi yaz:

 Bu soru, sağlanan resmi kaynaklarda cevaplanamamaktadır.
 """
        },
        {
            "role": "user",
            "content": f"""
 RESMİ KAYNAKLAR

 {context}

KULLANICININ SORUSU

{question}

Yalnızca yukarıdaki resmi kaynakları kullan.

Soruyla ilgili olan bilgileri kullan.

Cevabı en fazla 3 madde halinde ver.

Kaynaklarda cevap yoksa sadece şu cümleyi yaz:

Bu soru, sağlanan resmi kaynaklarda cevaplanamamaktadır.
"""
        }
    ]

    try:
        response = client.complete_chat(messages)
    except Exception as e:
        print("\n❌ Model cevap üretirken hata oluştu:")
        print(e)
        continue

    print("\n🤖 Asistanın Cevabı:\n")
    print(response.choices[0].message.content)

    print("\n📄 Kaynaklar:")

    sources = sorted(set(result["file_name"] for result in results))

    for source in sources:
        print(f"- {source}")