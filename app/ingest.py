import glob
import os

from app.rag import embed, get_connection

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

SCHEMA = """
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS chunks (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL
);
"""


def chunk_text(text: str) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start : start + CHUNK_SIZE].strip()
        if chunk:
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def main() -> None:
    with get_connection() as conn:
        conn.execute(SCHEMA)
        conn.execute("TRUNCATE chunks")

        for path in sorted(glob.glob("docs/kb/*.md")):
            source = os.path.basename(path)
            with open(path, encoding="utf-8") as f:
                pieces = chunk_text(f.read())

            vectors = embed(pieces)
            for piece, vector in zip(pieces, vectors):
                conn.execute(
                    "INSERT INTO chunks (source, content, embedding) VALUES (%s, %s, %s)",
                    (source, piece, vector),
                )
            print(f"{source}: {len(pieces)} chunks")

        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        print(f"total chunks in database: {count}")


if __name__ == "__main__":
    main()
