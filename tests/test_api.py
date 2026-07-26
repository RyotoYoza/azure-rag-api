from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def api_client():
    from app.main import app

    return TestClient(app)


def test_health_returns_ok(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_rejects_missing_question(api_client):
    response = api_client.post("/ask", json={})
    assert response.status_code == 422  # Pydantic validation error


def test_ask_returns_answer_and_sources(api_client, monkeypatch):
    # Fake retrieval: no database needed
    monkeypatch.setattr(
        "app.main.retrieve",
        lambda question, k=3: [("printer.md", "printer troubleshooting text")],
    )

    # Fake LLM: no Azure call, no cost, deterministic
    fake_completion = MagicMock()
    fake_completion.choices[0].message.content = "Restart the print spooler."
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value = fake_completion
    monkeypatch.setattr("app.main.client", fake_client)

    response = api_client.post("/ask", json={"question": "printer won't print"})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "Restart the print spooler."
    assert body["sources"] == ["printer.md"]
