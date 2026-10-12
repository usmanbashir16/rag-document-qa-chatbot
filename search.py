
from pathlib import Path

from read_pdf import extract_text_from_pdf
from chunk_text import chunk_text


def process_pdf(pdf_path: str) -> list[str]:
    """Extract text from a PDF and split it into chunks."""

    text = extract_text_from_pdf(pdf_path)

    chunks = chunk_text(
        text,
        chunk_size=500,
        overlap=50
    )

    return chunks


if __name__ == "__main__":
    pdf_path = input("Enter the PDF file path: ").strip().strip('"')

    try:
        chunks = process_pdf(pdf_path)

        print("\nPDF processed successfully!")
        print(f"Total chunks: {len(chunks)}")

        for index, chunk in enumerate(chunks, start=1):
            print(f"\n--- Chunk {index} ---")
            print(chunk[:300])
            print("...")

    except FileNotFoundError:
        print("Error: PDF file not found. Check the file path.")

    except Exception as error:
        print(f"Error processing PDF: {error}")