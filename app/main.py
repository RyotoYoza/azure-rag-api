import logging
import time

from fastapi import FastAPI
from pydantic import BaseModel

from app import config
from app.rag import client, retrieve

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("ragapi")

if config.APPINSIGHTS_CONNECTION_STRING:
    from azure.monitor.opentelemetry import configure_azure_monitor

    configure_azure_monitor(
        connection_string=config.APPINSIGHTS_CONNECTION_STRING,
        logger_name="ragapi",
    )
    logger.info("application insights configured")

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
    started = time.perf_counter()

    retrieval_started = time.perf_counter()
    chunks = retrieve(request.question, k=3)
    retrieval_ms = (time.perf_counter() - retrieval_started) * 1000

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
    usage = completion.usage

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    reasoning_tokens = 0
    details = getattr(usage, "completion_tokens_details", None)
    if details is not None:
        reasoning_tokens = getattr(details, "reasoning_tokens", 0) or 0

    cost_usd = (
        prompt_tokens / 1_000_000 * config.PRICE_INPUT_PER_1M
        + completion_tokens / 1_000_000 * config.PRICE_OUTPUT_PER_1M
    )

    answer = choice.message.content or ""
    total_ms = (time.perf_counter() - started) * 1000

    logger.info(
        "ask completed",
        extra={
            "question_length": len(request.question),
            "sources": ",".join(sorted({s for s, _ in chunks})),
            "chunks_retrieved": len(chunks),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "reasoning_tokens": reasoning_tokens,
            "total_tokens": usage.total_tokens,
            "cost_usd": round(cost_usd, 6),
            "finish_reason": choice.finish_reason,
            "answer_empty": not answer,
            "retrieval_ms": round(retrieval_ms, 1),
            "total_ms": round(total_ms, 1),
        },
    )

    if not answer:
        logger.warning(
            "empty answer returned",
            extra={
                "finish_reason": choice.finish_reason,
                "reasoning_tokens": reasoning_tokens,
            },
        )
        answer = "The model did not return an answer (token budget exhausted). Try rephrasing."

    return AskResponse(
        answer=answer,
        sources=sorted({source for source, _ in chunks}),
    )
