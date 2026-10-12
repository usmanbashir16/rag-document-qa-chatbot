
def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    """
    Split text into smaller chunks using words,
    with overlap between consecutive chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "Overlap must be at least 0 and smaller than chunk_size."
        )

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


if __name__ == "__main__":
    sample_text = input("Enter some text to test chunking: ")

    chunks = chunk_text(
        sample_text,
        chunk_size=10,
        overlap=2
    )

    print(f"\nTotal chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {index}:")
        print(chunk)