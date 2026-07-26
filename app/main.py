from fastapi import FastAPI
from pydantic import BaseModel

from app import config
from app.rag import client, retrieve

app = FastAPI(title="RAG API")

SYSTEM_PROMPT = """You are an IT support assistant.
Answer the question using ONLY the context below.
If the context does not contain the answer, say that you don't know.
Do not use outside knowledge.

Context:
{context}"""


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    chunks = retrieve(request.question, k=3)
    context = "\n\n---\n\n".join(f"[{source}]\n{content}" for source, content in chunks)

    completion = client.chat.completions.create(
        model=config.CHAT_DEPLOYMENT,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
            {"role": "user", "content": request.question},
        ],
        max_completion_tokens=2000,
    )

    choice = completion.choices[0]
    print("finish_reason:", choice.finish_reason, "| usage:", completion.usage)

    answer = choice.message.content or ""
    if not answer:
        answer = "The model did not return an answer (token budget exhausted). Try rephrasing."

    return AskResponse(
        answer=answer,
        sources=sorted({source for source, _ in chunks}),
    )
