from app.ingest import chunk_text, CHUNK_OVERLAP


def test_empty_text_produces_no_chunks():
    assert chunk_text("") == []


def test_short_text_is_a_single_chunk():
    chunks = chunk_text("just a short sentence")
    assert len(chunks) == 1
    assert chunks[0] == "just a short sentence"


def test_long_text_splits_into_multiple_chunks():
    text = "a" * 2000
    chunks = chunk_text(text)
    assert len(chunks) > 1


def test_consecutive_chunks_overlap():
    # digits 0-9 repeating, so every position is identifiable
    text = "".join(str(i % 10) for i in range(2000))
    chunks = chunk_text(text)
    # the last CHUNK_OVERLAP chars of chunk 0 must reappear at the start of chunk 1
    assert chunks[0][-CHUNK_OVERLAP:] == chunks[1][:CHUNK_OVERLAP]
