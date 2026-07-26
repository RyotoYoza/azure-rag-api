import os

# Set dummy config BEFORE any app module is imported.
# These never make real calls — the LLM and DB are mocked in the tests.
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com/")
os.environ.setdefault("AZURE_OPENAI_API_KEY", "test-key")
os.environ.setdefault("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
os.environ.setdefault("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-5-mini")
os.environ.setdefault("AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-3-small")
os.environ.setdefault("DATABASE_URL", "postgresql://u:p@localhost:5432/testdb")
