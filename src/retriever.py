import json
import re
import sqlite3
from pathlib import Path

import numpy as np

from src.embedding import load_embedding_model, create_embedding

DATABASE_PATH = Path("database/rag.db")

embedding_client = None


def cosine_similarity(vector1, vector2):
    vector1 = np.array(vector1, dtype=np.float32)
    vector2 = np.array(vector2, dtype=np.float32)

    denominator = np.linalg.norm(vector1) * np.linalg.norm(vector2)

    if denominator == 0:
        return 0.0

    return float(np.dot(vector1, vector2) / denominator)


def create_query_embedding(query):
    global embedding_client

    if embedding_client is None:
        embedding_client = load_embedding_model()

    return create_embedding(embedding_client, query)


def keyword_score(query, text):
    query_words = re.findall(r"\w+", query.lower())
    text = text.lower()

    score = 0

    for word in query_words:
        if len(word) < 3:
            continue

        if word in text:
            score += 0.10

    return score


def search_chunks(query, allowed_files=None):

    query_embedding = create_query_embedding(query)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    if allowed_files:
        placeholders = ",".join("?" for _ in allowed_files)

        cursor.execute(
            f"""
            SELECT file_name, chunk_text, embedding
            FROM chunks
            WHERE file_name IN ({placeholders})
            """,
            allowed_files
        )
    else:
        cursor.execute("""
            SELECT file_name, chunk_text, embedding
            FROM chunks
        """)

    rows = cursor.fetchall()
    connection.close()

    results = []
    seen = set()

    for file_name, chunk_text, embedding_json in rows:

        try:
            chunk_embedding = json.loads(embedding_json)
        except Exception:
            continue

        semantic = cosine_similarity(query_embedding, chunk_embedding)
        keyword = keyword_score(query, chunk_text)

        results.append({
            "file_name": file_name,
            "chunk_text": chunk_text,
            "score": semantic + keyword
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    filtered = []

    for item in results:

        if item["chunk_text"] in seen:
            continue

        seen.add(item["chunk_text"])
        filtered.append(item)

        if len(filtered) == 3:
            break

    return filtered