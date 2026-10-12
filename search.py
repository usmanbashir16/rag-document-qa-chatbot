
from vector_store import search_similar


def main() -> None:
    print("RFP Document Search")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Ask a question about your RFP: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            results = search_similar(question, n_results=3)

            if not results:
                print("No results found. Ingest a PDF first.")
                continue

            print("\nRelevant information:\n")

            for index, result in enumerate(results, start=1):
                source = result["metadata"]["source"]
                chunk_index = result["metadata"]["chunk_index"]
                distance = result["distance"]

                print(f"--- Result {index} ---")
                print(f"Source: {source}")
                print(f"Chunk: {chunk_index}")
                print(f"Distance: {distance:.4f}")
                print(result["text"])
                print()

        except Exception as error:
            print(f"Search error: {error}")


if __name__ == "__main__":
    main()