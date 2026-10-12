
from sentence_transformers import SentenceTransformer


# A small, commonly used model for text embeddings.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model() -> SentenceTransformer:
    """Load the embedding model."""
    return SentenceTransformer(MODEL_NAME)


def create_embeddings(
    texts: list[str],
    model: SentenceTransformer | None = None
) -> list[list[float]]:
    """Convert text chunks into numerical vectors."""

    if not texts:
        return []

    if model is None:
        model = load_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings.tolist()


if __name__ == "__main__":
    sample_texts = [
        "The tender submission deadline is 25 September.",
        "The supplier must provide technical support.",
        "The bid security amount is two million rupees."
    ]

    try:
        model = load_embedding_model()
        embeddings = create_embeddings(sample_texts, model)

        print("\nEmbeddings created successfully!")
        print(f"Total text samples: {len(embeddings)}")
        print(f"Vector dimensions: {len(embeddings[0])}")
        print("\nFirst vector (first 10 numbers):")
        print(embeddings[0][:10])

    except Exception as error:
        print(f"Error creating embeddings: {error}")