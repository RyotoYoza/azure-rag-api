import json
import os
import sys
from pathlib import Path

import httpx

BASE_URL = os.environ["EVAL_BASE_URL"].rstrip("/")
THRESHOLD = float(os.environ.get("EVAL_THRESHOLD", "0.85"))
DATASET = Path(__file__).parent / "dataset.json"

REFUSAL_MARKERS = [
    "don't know",
    "do not know",
    "not contain",
    "no information",
    "cannot answer",
    "context does not",
]


def ask(question: str) -> dict:
    response = httpx.post(
        f"{BASE_URL}/ask",
        json={"question": question},
        timeout=120.0,
    )
    response.raise_for_status()
    return response.json()


def score_grounded(case: dict, result: dict) -> tuple[bool, bool, str]:
    sources = result.get("sources", [])
    answer = (result.get("answer") or "").lower()

    retrieved = case["expected_source"] in sources
    contains = all(kw.lower() in answer for kw in case.get("must_contain", []))

    notes = []
    if not retrieved:
        notes.append(f"expected {case['expected_source']}, got {sources}")
    if not contains:
        missing = [kw for kw in case["must_contain"] if kw.lower() not in answer]
        notes.append(f"missing keywords: {missing}")
    if not answer:
        notes.append("EMPTY ANSWER")

    return retrieved, contains, "; ".join(notes)


def score_refusal(result: dict) -> tuple[bool, str]:
    answer = (result.get("answer") or "").lower()
    refused = any(marker in answer for marker in REFUSAL_MARKERS)
    return refused, "" if refused else f"answered instead of refusing: {answer[:80]}"


def main() -> None:
    cases = json.loads(DATASET.read_text())["cases"]

    retrieval_pass = retrieval_total = 0
    answer_pass = answer_total = 0
    failures = []

    print(f"Running {len(cases)} eval cases against {BASE_URL}\n")

    for case in cases:
        try:
            result = ask(case["question"])
        except Exception as exc:
            failures.append(f"[{case['id']}] request failed: {exc}")
            answer_total += 1
            continue

        if case["type"] == "grounded":
            retrieved, contains, notes = score_grounded(case, result)
            retrieval_total += 1
            answer_total += 1
            retrieval_pass += retrieved
            answer_pass += contains
            status = "PASS" if (retrieved and contains) else "FAIL"
            if status == "FAIL":
                failures.append(f"[{case['id']}] {notes}")
        else:
            refused, notes = score_refusal(result)
            answer_total += 1
            answer_pass += refused
            status = "PASS" if refused else "FAIL"
            if status == "FAIL":
                failures.append(f"[{case['id']}] {notes}")

        print(f"{status}  {case['id']}")

    retrieval_score = retrieval_pass / retrieval_total if retrieval_total else 1.0
    answer_score = answer_pass / answer_total if answer_total else 0.0

    print(f"\nRetrieval accuracy: {retrieval_score:.1%} ({retrieval_pass}/{retrieval_total})")
    print(f"Answer accuracy:    {answer_score:.1%} ({answer_pass}/{answer_total})")
    print(f"Threshold:          {THRESHOLD:.0%}")

    if failures:
        print("\nFailures:")
        for failure in failures:
            print(f"  - {failure}")

    if answer_score < THRESHOLD or retrieval_score < THRESHOLD:
        print("\nEVAL GATE FAILED")
        sys.exit(1)

    print("\nEVAL GATE PASSED")


if __name__ == "__main__":
    main()
