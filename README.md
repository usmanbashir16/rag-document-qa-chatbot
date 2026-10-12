<img width="1910" height="996" alt="image" src="https://github.com/user-attachments/assets/7a353ab7-e248-4721-a82d-6f41c17fce49" />
**RAG Document Q&A Chatbot with Vector Database**

An AI-powered document question-answering application that allows users to ask questions about PDF documents and receive context-aware answers using Retrieval-Augmented Generation (RAG).

The project combines a React frontend, FastAPI backend, semantic search, ChromaDB vector storage, and Google's Gemini API to retrieve relevant document content and generate answers based on the available context.

## Features

* **PDF-Based Question Answering:** Ask natural-language questions about indexed PDF documents.
* **Retrieval-Augmented Generation (RAG):** Retrieves relevant document chunks before generating an answer.
* **Semantic Search:** Uses sentence embeddings to identify content related to a question.
* **Vector Database:** Stores and searches document embeddings using ChromaDB.
* **AI-Generated Responses:** Uses Google's Gemini API to generate context-aware answers.
* **Source References:** Returns relevant document chunks to help users understand where answers came from.
* **Interactive Web Interface:** React-based chatbot interface for submitting questions and viewing responses.
* **REST API:** FastAPI endpoints connect the frontend with the RAG pipeline.

## Technology Stack

| Component       | Technology                                 |
| --------------- | ------------------------------------------ |
| Frontend        | React.js, Vite, JavaScript, CSS            |
| Backend         | Python, FastAPI                            |
| Vector Database | ChromaDB                                   |
| Embedding Model | Sentence Transformers — `all-MiniLM-L6-v2` |
| Generative AI   | Google Gemini API                          |
| API Server      | Uvicorn                                    |
| Version Control | Git and GitHub                             |

## How It Works

1. **Document Processing:** PDF documents are extracted and divided into smaller text chunks.
2. **Embedding Generation:** A sentence-transformer model converts text chunks into numerical vector embeddings.
3. **Vector Storage:** ChromaDB stores the embeddings and associated document text.
4. **Question Submission:** The user enters a question through the React interface.
5. **Semantic Retrieval:** The backend searches the vector database for relevant document chunks.
6. **Answer Generation:** Retrieved context is sent to the Gemini API to generate a relevant response.
7. **Source Display:** The application returns the answer along with relevant source information.

## Project Structure

```text
rag-document-qa-VectorDB/
├── backend/
│   └── api.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── chroma_db/             # Local vector database (not committed)
├── .env                   # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

Additional PDF-processing and vector-store Python files may exist in the project root.

## Prerequisites

Install the following before running the project:

* Python 3.12 or a compatible version
* Node.js and npm
* Git
* A Google Gemini API key

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/usmanbashir16/rag-document-qa-chatbot.git
cd rag-document-qa-VectorDB
```

### 2. Set Up the Python Environment

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace the placeholder with your actual Gemini API key. Use a model name supported by your Gemini API account.

**Security:** Never commit your `.env` file or expose your API key in frontend code.

### 4. Prepare the Vector Database

Process and index your PDF documents using the project's existing PDF-processing and vector-store workflow. Ensure the ChromaDB collection is populated before asking document-specific questions.

The local `chroma_db/` directory is generated data and is not included in the Git repository.

### 5. Start the Backend

From the project root, activate your Python environment and run:

```bash
python -m uvicorn backend.api:app --reload
```

The backend should be available at:

* API server: http://127.0.0.1:8000
* Interactive API documentation: http://127.0.0.1:8000/docs
* Health check: http://127.0.0.1:8000/health

### 6. Start the Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, normally:

http://localhost:5173

Keep both the frontend and backend servers running while using the chatbot.

## API Endpoints

| Method | Endpoint    | Purpose                                                            |
| ------ | ----------- | ------------------------------------------------------------------ |
| GET    | `/health`   | Checks backend health                                              |
| POST   | `/api/chat` | Accepts a question and returns an AI-generated answer with sources |
| GET    | `/docs`     | Opens the interactive FastAPI documentation                        |

### Example Chat Request

```json
{
  "question": "What does the document say about the main topic?"
}
```

The response contains an answer and relevant source information. The exact response structure depends on the backend implementation.

## Security and Privacy

* Store API keys in environment variables.
* Keep `.env`, private PDFs, virtual environments, and local vector database files out of GitHub.
* Avoid uploading confidential or sensitive documents to external AI services without authorization.
* Review document content and API data-handling requirements before using the application with business or customer information.

## Future Improvements

* Support multiple documents and document collections.
* Add document upload and indexing through the web interface.
* Improve source citations and retrieval accuracy.
* Add conversation history and session management.
* Introduce authentication and user-level access control.
* Deploy the frontend and backend for remote access.

## Author

**Muhammad Usman**

GitHub: https://github.com/usmanbashir16

---

*Built as a practical project to explore Retrieval-Augmented Generation, semantic search, vector databases, LLM integration, and full-stack AI application development.*

