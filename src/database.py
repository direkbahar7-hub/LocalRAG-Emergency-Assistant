import sqlite3
from pathlib import Path
import json

DATABASE_PATH = Path("database/rag.db")


def create_database():
    """
    SQLite veritabanını oluşturur.
    Eğer yoksa chunks tablosunu oluşturur.
    """

    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            chunk_text TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("SQLite veritabanı hazır.")


def insert_chunks(chunks):
    """
    Embedding'leri SQLite veritabanına kaydeder.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM chunks")

    for chunk in chunks:
        cursor.execute(
            """
            INSERT INTO chunks (file_name, chunk_text, embedding)
            VALUES (?, ?, ?)
            """,
            (
                chunk["file_name"],
                chunk["text"],
                json.dumps(chunk["embedding"])
            )
        )

    connection.commit()
    connection.close()

    print(f"{len(chunks)} chunk veritabanına kaydedildi.")

def get_all_chunks():
    """
    Veritabanındaki tüm kayıtları döndürür.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT file_name, chunk_text, embedding
        FROM chunks
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows