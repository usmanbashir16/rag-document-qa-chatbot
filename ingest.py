
from pathlib import Path

from read_pdf import extract_text_from_pdf
from chunk_text import chunk_text
from embeddings import load_embedding_model, create_embeddings
from vector_store import store_chunks


def ingest_pdf(pdf_path: str) -> None:
    """Read a PDF, create chunks and embeddings, and store them."""

    pdf_file = Path(pdf_path)

    if not pdf_file.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_file}")

    print("\nStep 1: Extracting text from PDF...")
    text = extract_text_from_pdf(str(pdf_file))

    print("\nStep 2: Splitting text into chunks...")
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    print(f"Total chunks created: {len(chunks)}")

    print("\nStep 3: Loading embedding model...")
    model = load_embedding_model()

    print("\nStep 4: Creating embeddings...")
    embeddings = create_embeddings(chunks, model)

    print("\nStep 5: Saving chunks to ChromaDB...")
    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        source_name=pdf_file.name
    )

    print("\nPDF ingestion completed successfully!")


if __name__ == "__main__":
    pdf_path = input("Enter the PDF file path: ").strip().strip('"')

    try:
        ingest_pdf(pdf_path)

    except Exception as error:
        print(f"\nError during PDF ingestion: {error}")