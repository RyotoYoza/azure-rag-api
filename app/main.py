from fastapi import FastAPI
from openai import AzureOpenAI
from pydantic import BaseModel

from app import config

app = FastAPI(title="RAG API")

client = AzureOpenAI(
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    api_key=config.AZURE_OPENAI_API_KEY,
    api_version=config.AZURE_OPENAI_API_VERSION,
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    completion = client.chat.completions.create(
        model=config.CHAT_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are an IT support assistant. Answer concisely."},
            {"role": "user", "content": request.question},
        ],
        max_completion_tokens=800,
    )
    return AskResponse(answer=completion.choices[0].message.content)
