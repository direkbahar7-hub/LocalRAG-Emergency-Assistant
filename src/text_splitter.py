def split_text(text):

    chunks = []

    current = ""

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Tek başına sayfa numaralarını at
        if line.isdigit():
            continue

        # Çok kısa satırları at
        if len(line) < 3:
            continue

        # Yeni büyük başlık gelirse önceki chunk'ı bitir
        if (
            line.isupper()
            and len(line) < 80
            and current
        ):
            chunks.append(current.strip())
            current = line

        else:
            current += "\n" + line

    if current:
        chunks.append(current.strip())

    return chunks