from pathlib import Path
from pypdf import PdfReader


def load_all_pdfs(folder_path):
    documents = []

    pdf_files = Path(folder_path).rglob("*.pdf")

    for pdf_file in pdf_files:
        print(f"Okunuyor: {pdf_file.name}")

        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        documents.append({
            "file_name": pdf_file.name,
            "file_path": str(pdf_file),
            "text": text
        })

    return documents