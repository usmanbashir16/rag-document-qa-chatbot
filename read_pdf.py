
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from all pages of a PDF file."""

    reader = PdfReader(pdf_path)
    extracted_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            extracted_text.append(text)

        print(f"Processed page {page_number}/{len(reader.pages)}")

    full_text = "\n".join(extracted_text)

    if not full_text.strip():
        raise ValueError(
            "No readable text found. The PDF may contain scanned images."
        )

    return full_text


if __name__ == "__main__":
    pdf_path = input("Enter the PDF file path: ").strip().strip('"')

    try:
        text = extract_text_from_pdf(pdf_path)

        print("\nPDF text extracted successfully!")
        print(f"Total characters: {len(text)}")
        print("\nFirst 1000 characters:\n")
        print(text[:1000])

    except FileNotFoundError:
        print("Error: PDF file not found. Check the file path.")

    except Exception as error:
        print(f"Error reading PDF: {error}")