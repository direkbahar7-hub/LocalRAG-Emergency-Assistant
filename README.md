🚨 LocalRAG Emergency Assistant
Yerel (Offline) çalışan, AFAD ve MEB tarafından yayımlanan resmi dokümanları kullanarak Türkçe sorulara cevap verebilen bir Retrieval-Augmented Generation (RAG) uygulamasıdır.

Bu proje, Microsoft Yaz Eğitim Programı kapsamında geliştirilmiştir.

---

🚀 Özellikler

Resmi AFAD ve MEB dokümanlarını kullanır
Microsoft Foundry Local SDK ile çalışır
Phi-3.5 Mini + Qwen3 Embedding
SQLite Vektör Veritabanı
Tamamen Offline
Türkçe soru-cevap desteği

---

 🛠️ Kullanılan Teknolojiler

Python
Microsoft Foundry Local SDK
Phi-3.5 Mini
Qwen3 Embedding 0.6B
SQLite
PyPDF

---

 📂 Proje Yapısı

LocalRAG-Emergency-Assistant
│
├── documents/
├── database/
├── src/
├── build_database.py
├── chat.py
└── requirements.txt


---

 ▶️ Kurulum

pip install -r requirements.txt
python build_database.py
python chat.py


---

 💬 Örnek

Soru

Deprem sırasında ne yapmalıyım?


Cevap

• Çök-Kapan-Tutun hareketini uygulayın.
• Sakin olun.
• Resmi kurumların yönlendirmelerini takip edin.


---

 👨‍💻 Geliştiriciler

Muhammed Ali UZUN
Bahar DİREK


---

 📄 Not

Bu proje eğitim amacıyla geliştirilmiştir.
