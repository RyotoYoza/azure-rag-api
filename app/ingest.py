from pathlib import Path

from app.rag import embed, get_connection

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

KB_DIR = Path(__file__).resolve().parent.parent / "docs" / "kb"

SCHEMA = """
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
    files = sorted(KB_DIR.glob("*.md"))
    if not files:
        raise SystemExit(f"No .md files found in {KB_DIR}")

    with get_connection() as conn:
        conn.execute(SCHEMA)
        conn.execute("TRUNCATE chunks")

        total = 0
        for path in files:
            pieces = chunk_text(path.read_text(encoding="utf-8"))
            vectors = embed(pieces)
            for piece, vector in zip(pieces, vectors):
                conn.execute(
                    "INSERT INTO chunks (source, content, embedding) VALUES (%s, %s, %s)",
                    (path.name, piece, vector),
                )
            total += len(pieces)
            print(f"{path.name}: {len(pieces)} chunks")

        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        print(f"total chunks in database: {count}")
        if count != total:
            print(f"WARNING: inserted {total} but table holds {count}")


if __name__ == "__main__":
    main()
