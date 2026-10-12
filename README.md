<img width="1910" height="996" alt="image" src="https://github.com/user-attachments/assets/7a353ab7-e248-4721-a82d-6f41c17fce49" />
# RAG Document Q&A Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about PDF documents using semantic search, vector embeddings, ChromaDB, and the Gemini API.

The project extracts text from PDF documents, splits it into smaller chunks, converts the chunks into numerical embeddings, and stores them in a persistent vector database. When a user asks a question, the system retrieves relevant document sections and uses Gemini to generate an answer based on the retrieved context.

## Features

* PDF text extraction using PyPDF
* Text chunking with overlapping sections
* Text embeddings using Sentence Transformers
* Persistent vector storage with ChromaDB
* Semantic search for relevant document sections
* Gemini-powered question answering
* Support for ingesting multiple PDF documents into one collection

## Tech Stack

* Python
* PyPDF
* Sentence Transformers
* ChromaDB
* Google Gemini API
* python-dotenv

## Project Structure

```text
rag-document-qa-VectorDB/
├── read_pdf.py
├── chunk_text.py
├── embeddings.py
├── vector_store.py
├── ingest.py
├── search.py
├── chat.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The `chroma_db/` directory is created locally when the vector database is initialized. It is excluded from Git tracking.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/usmanbashir16/rag-document-qa-chatbot.git
cd rag-document-qa-chatbot
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv ai-env
```

On Windows PowerShell:

```powershell
.\ai-env\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Create a `.env` file in the project root directory and add your Gemini API key:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key. Never commit your `.env` file or expose your API key publicly.

## How to Use

### Step 1: Add a PDF

Place your PDF document in the project directory or keep it at another accessible location.

### Step 2: Ingest the PDF

Run:

```bash
python ingest.py
```

Enter the PDF's full path when prompted.

The ingestion pipeline automatically:

1. Extracts text from the PDF.
2. Splits the text into chunks.
3. Generates embeddings for the chunks.
4. Stores the chunks, embeddings, and source metadata in ChromaDB.

### Step 3: Ask Questions

Run:

```bash
python chat.py
```

Enter questions related to the ingested documents. The chatbot retrieves relevant text chunks and uses Gemini to generate answers.

Type `exit` to quit the chatbot.

### Optional: Search Without Gemini

To inspect retrieved text chunks without generating a Gemini answer, run:

```bash
python search.py
```

## How the RAG Pipeline Works

```text
PDF Document
     |
     v
Text Extraction
     |
     v
Text Chunking
     |
     v
Embedding Generation
     |
     v
ChromaDB Vector Storage
     |
     v
User Question
     |
     v
Semantic Retrieval
     |
     v
Relevant Document Context
     |
     v
Gemini API
     |
     v
Generated Answer
```

## Configuration

* **Chunk size:** 500 words
* **Chunk overlap:** 50 words
* **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`
* **Vector database:** ChromaDB
* **Generative model:** Configured in `chat.py`

These settings can be adjusted according to document length, retrieval quality, and model availability.

## Important Notes

* The vector database is stored locally in `chroma_db/`.
* Previously ingested documents remain available in the persistent collection unless the database is removed or modified.
* Multiple PDFs currently share the same collection, so retrieved results may come from different documents.
* Scanned PDFs may require OCR because ordinary PDF text extraction may not read text embedded in images.
* Generated answers depend on the retrieved document context and should be verified against the original document for critical requirements, deadlines, and compliance information.
* Do not commit API keys, confidential documents, or private database files to GitHub.

## Future Improvements

* PDF page-number citations
* Improved handling of tables, headings, and document structure
* Source filtering for individual documents
* A web-based chatbot interface
* Better retrieval evaluation and testing

## License

Add a license if you intend to distribute this project publicly.
