
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel, Field

# Ensure imports work when starting the API from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from vector_store import search_similar  # noqa: E402


MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

app = FastAPI(
    title="RAG Document Q&A API",
    description="Ask questions about documents indexed in ChromaDB.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


class Source(BaseModel):
    name: str
    chunk: str
    text: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


def flatten_chroma_values(value: Any) -> list:
    """Flatten ChromaDB's usual one-query nested result lists."""
    if value is None:
        return []
    if isinstance(value, list) and value and isinstance(value[0], list):
        return value[0]
    if isinstance(value, list):
        return value
    return []


def normalize_results(results: Any) -> list[dict]:
    """
    Support common return formats:
    - ChromaDB-style dictionaries
    - (documents, metadatas, distances) tuples
    - Lists of dictionaries or text chunks
    """
    if isinstance(results, dict):
        documents = flatten_chroma_values(
            results.get("documents") or results.get("chunks")
        )
        metadatas = flatten_chroma_values(results.get("metadatas"))
        distances = flatten_chroma_values(results.get("distances"))

        if documents:
            return [
                {
                    "text": str(doc),
                    "metadata": (
                        metadatas[i]
                        if i < len(metadatas) and isinstance(metadatas[i], dict)
                        else {}
                    ),
                    "distance": distances[i] if i < len(distances) else None,
                }
                for i, doc in enumerate(documents)
                if doc
            ]

    if isinstance(results, tuple) and results:
        documents = flatten_chroma_values(results[0])
        metadatas = (
            flatten_chroma_values(results[1])
            if len(results) > 1 else []
        )
        distances = (
            flatten_chroma_values(results[2])
            if len(results) > 2 else []
        )

        return [
            {
                "text": str(doc),
                "metadata": (
                    metadatas[i]
                    if i < len(metadatas) and isinstance(metadatas[i], dict)
                    else {}
                ),
                "distance": distances[i] if i < len(distances) else None,
            }
            for i, doc in enumerate(documents)
            if doc
        ]

    if isinstance(results, list):
        normalized = []

        for item in results:
            if isinstance(item, str):
                normalized.append({
                    "text": item,
                    "metadata": {},
                    "distance": None,
                })
            elif isinstance(item, dict):
                chunk_text = (
                    item.get("text")
                    or item.get("chunk")
                    or item.get("document")
                    or item.get("page_content")
                )

                if chunk_text:
                    normalized.append({
                        "text": str(chunk_text),
                        "metadata": item.get("metadata", {}),
                        "distance": item.get("distance"),
                    })

        return normalized

    return []


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "RAG API is running"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question.",
        )

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is missing from your .env file.",
        )

    try:
        # Retrieve relevant chunks from your existing ChromaDB.
        raw_results = search_similar(question, n_results=5)
        results = normalize_results(raw_results)

        if not results:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No relevant document chunks were found. "
                    "Please ingest a PDF first or check your vector store."
                ),
            )

        context_parts = []
        sources = []

        for i, result in enumerate(results, start=1):
            text = result["text"]
            metadata = result["metadata"]

            source_name = (
                metadata.get("source_name")
                or metadata.get("source")
                or metadata.get("filename")
                or metadata.get("file_name")
                or "Indexed document"
            )

            chunk_index = metadata.get(
                "chunk_index",
                metadata.get("chunk_id", i),
            )

            context_parts.append(
                f"[Source {i}: {source_name}, chunk {chunk_index}]\n{text}"
            )

            sources.append(Source(
                name=str(source_name),
                chunk=str(chunk_index),
                text=text[:500],
            ))

        context = "\n\n".join(context_parts)

        prompt = f"""
You are a helpful document question-answering assistant.

Answer the user's question using the supplied document context.
- Use the context as your primary source of information.
- Do not invent facts that are not supported by the context.
- If the context does not contain the answer, clearly say so.
- Give a clear, useful answer.
- Refer to source numbers such as [Source 1] when appropriate.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        answer = response.text
        if not answer:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an empty response.",
            )

        return ChatResponse(
            answer=answer,
            sources=sources,
        )

    except HTTPException:
        raise
    except Exception as exc:
        print(f"RAG API error: {exc}")
        raise HTTPException(
            status_code=500,
            detail=(
                "The chatbot could not process your question. "
                "Check the backend terminal for the error."
            ),
        ) from exc