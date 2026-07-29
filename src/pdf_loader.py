from pathlib import Path
from pypdf import PdfReader


def clean_page(text: str):
    """
    Sayfa numaralarını ve gereksiz boşlukları temizler.
    """

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Sadece sayılardan oluşan satırlar (sayfa numarası)
        if line.isdigit():
            continue

        lines.append(line)

    return "\n".join(lines)


def load_all_pdfs(folder_path):

    documents = []

    pdf_files = Path(folder_path).rglob("*.pdf")

    for pdf_file in pdf_files:

        print(f"Okunuyor: {pdf_file.name}")

        reader = PdfReader(pdf_file)

        # HER SAYFA AYRI DOKÜMAN
        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if not text:
                continue

            text = clean_page(text)

            if len(text) < 30:
                continue

            documents.append({
                "file_name": pdf_file.name,
                "page": page_number,
                "text": text
            })

    return documents