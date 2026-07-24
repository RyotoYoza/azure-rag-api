import numpy as np
import psycopg
from openai import AzureOpenAI
from pgvector.psycopg import register_vector

from app import config

client = AzureOpenAI(
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    api_key=config.AZURE_OPENAI_API_KEY,
    api_version=config.AZURE_OPENAI_API_VERSION,
)


def embed(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model=config.EMBED_DEPLOYMENT,
        input=texts,
    )
    return [item.embedding for item in response.data]


def get_connection():
    conn = psycopg.connect(config.DATABASE_URL)
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()
    register_vector(conn)
    return conn


def retrieve(question: str, k: int = 5) -> list[tuple[str, str]]:
    question_vector = np.array(embed([question])[0])
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT source, content FROM chunks ORDER BY embedding <=> %s LIMIT %s",
            (question_vector, k),
        ).fetchall()
    return rows
