
import os

from dotenv import load_dotenv
from google import genai

from vector_store import search_similar


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.5-flash-lite"


def generate_answer(question: str) -> None:
    """Retrieve relevant chunks and generate a grounded answer."""

    # Step 1: Retrieve relevant text from ChromaDB
    results = search_similar(question, n_results=5)

    if not results:
        print("\nNo relevant information found.")
        print("Please ingest your PDF first using: python ingest.py")
        return

    # Step 2: Prepare the retrieved context
    context_parts = []

    for index, result in enumerate(results, start=1):
        source = result["metadata"]["source"]
        chunk_index = result["metadata"]["chunk_index"]

        context_parts.append(
            f"[Source {index}: {source}, Chunk {chunk_index}]\n"
            f"{result['text']}"
        )

    context = "\n\n".join(context_parts)

    # Step 3: Ask Gemini to answer using the retrieved context
    prompt = f"""
You are a helpful assistant for answering questions about RFP documents.

Answer the user's question using ONLY the provided document context.

Rules:
- Do not invent facts, dates, amounts, or requirements.
- If the context does not contain the answer, clearly say:
  "I could not find this information in the retrieved document sections."
- Keep the answer clear and easy to understand.
- Include source references such as [Source 1] in your answer.
- Distinguish between explicit facts and any reasonable interpretation.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    print("\nAnswer:\n")
    print(response.text or "Gemini did not return a text answer.")

    print("\nRetrieved sources:")

    for index, result in enumerate(results, start=1):
        source = result["metadata"]["source"]
        chunk_index = result["metadata"]["chunk_index"]

        print(f"[Source {index}] {source} — Chunk {chunk_index}")


def main() -> None:
    if not API_KEY:
        print("GEMINI_API_KEY not found.")
        print("Please check your .env file.")
        return

    print("RFP RAG Chatbot")
    print("Ask questions about your indexed PDF.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            generate_answer(question)

        except Exception as error:
            print(f"\nError: {error}")

        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()