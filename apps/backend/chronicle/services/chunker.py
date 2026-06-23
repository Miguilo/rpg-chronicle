def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[dict]:
    """Split texts into chunks"""
    chunks = []
    if not text:
        return chunks

    chunk_index = 0

    for chunk_index, chunk_start_id in enumerate(range(0, len(text), chunk_size-overlap)):
        chunks.append({"content": text[chunk_start_id:chunk_start_id+chunk_size],
                        "chunk_index": chunk_index})

    return chunks

