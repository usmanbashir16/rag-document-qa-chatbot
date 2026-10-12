
import chromadb
from pathlib import Path

from embeddings import create_embeddings, load_embedding_model


# Store the database inside the project folder.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "chroma_db"

COLLECTION_NAME = "rfp_documents"


def get_collection():
    """Create or open the persistent ChromaDB collection."""

    client = chromadb.PersistentClient(path=str(DB_PATH))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    source_name: str
) -> None:
    """Save text chunks, embeddings, and source information."""

    if len(chunks) != len(embeddings):
        raise ValueError(
            "The number of chunks and embeddings must be equal."
        )

    if not chunks:
        print("No chunks to store.")
        return

    collection = get_collection()

    ids = [
        f"{source_name}_{index}"
        for index in range(len(chunks))
    ]

    metadatas = [
        {
            "source": source_name,
            "chunk_index": index
        }
        for index in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")


def search_similar(
    query: str,
    n_results: int = 3
) -> list[dict]:
    """Find text chunks that are semantically similar to a question."""

    collection = get_collection()

    if collection.count() == 0:
        print("The vector database is empty. Store some chunks first.")
        return []

    model = load_embedding_model()

    query_embedding = create_embeddings(
        [query],
        model
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    matches = []

    for index, document in enumerate(results["documents"][0]):
        matches.append({
            "text": document,
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index]
        })

    return matches


if __name__ == "__main__":
    collection = get_collection()

    print("ChromaDB initialized successfully!")
    print(f"Database location: {DB_PATH}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Stored chunks: {collection.count()}")