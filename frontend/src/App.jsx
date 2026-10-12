import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
const [question, setQuestion] = useState("");
const [messages, setMessages] = useState([]);
const [loading, setLoading] = useState(false);
const [apiStatus, setApiStatus] = useState("checking");

useEffect(() => {
let active = true;


fetch(`${API_URL}/health`)
  .then((response) => {
    if (!response.ok) throw new Error("API unavailable");
    return response.json();
  })
  .then(() => {
    if (active) setApiStatus("online");
  })
  .catch(() => {
    if (active) setApiStatus("offline");
  });

return () => {
  active = false;
};


}, []);

async function sendQuestion(event) {
event.preventDefault();


const cleanQuestion = question.trim();
if (!cleanQuestion || loading) return;

setMessages((previous) => [
  ...previous,
  { role: "user", text: cleanQuestion },
]);
setQuestion("");
setLoading(true);

try {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: cleanQuestion }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Something went wrong. Please try again."
    );
  }

  setMessages((previous) => [
    ...previous,
    {
      role: "assistant",
      text: data.answer,
      sources: data.sources || [],
    },
  ]);
} catch (error) {
  setMessages((previous) => [
    ...previous,
    {
      role: "error",
      text:
        error.message ||
        "Could not connect to the backend. Check that the API is running.",
    },
  ]);
} finally {
  setLoading(false);
}


}

function clearChat() {
if (loading) return;
setMessages([]);
setQuestion("");
}

return ( <div className="app-shell"> <aside className="sidebar"> <div className="brand"> <div className="brand-icon">D</div> <div> <h1>DocuMind</h1> <p>Document Intelligence</p> </div> </div>


    <button className="new-chat" onClick={clearChat} disabled={loading}>
      <span>＋</span> New conversation
    </button>

    <div className="sidebar-section">
      <p className="section-label">YOUR WORKSPACE</p>
      <div className="sidebar-item active">
        <span>▤</span> Document Q&amp;A
      </div>
      <div className="sidebar-item">
        <span>⌘</span> Retrieval augmented generation
      </div>
    </div>

    <div className="sidebar-bottom">
      <div className="status-row">
        <span className={`status-dot ${apiStatus}`} />
        <span>
          {apiStatus === "checking"
            ? "Checking API..."
            : apiStatus === "online"
              ? "Backend connected"
              : "Backend offline"}
        </span>
      </div>
      <p>Powered by your documents and AI</p>
    </div>
  </aside>

  <main className="main-panel">
    <header className="topbar">
      <div>
        <p className="topbar-label">WORKSPACE / DOCUMENT Q&amp;A</p>
        <h2>AI Document Assistant</h2>
      </div>
      <div className="api-badge">
        <span className={`status-dot ${apiStatus}`} />
        {apiStatus === "online"
          ? "API Online"
          : apiStatus === "checking"
            ? "Connecting"
            : "API Offline"}
      </div>
    </header>

    <section className="chat-area">
      {messages.length === 0 ? (
        <div className="welcome">
          <div className="welcome-icon">✳</div>
          <p className="eyebrow">YOUR KNOWLEDGE, CONNECTED</p>
          <h3>Ask your documents<br />anything.</h3>
          <p className="welcome-description">
            Ask questions about your indexed PDFs. DocuMind retrieves
            relevant passages and uses them to generate an answer.
          </p>

          <div className="suggestions">
            <button
              onClick={() =>
                setQuestion("Summarize the main points of my document.")
              }
            >
              <span>↗</span>
              <div>
                <strong>Summarize a document</strong>
                <small>Get the key points and ideas</small>
              </div>
            </button>

            <button
              onClick={() =>
                setQuestion("What are the most important findings?")
              }
            >
              <span>⌕</span>
              <div>
                <strong>Find key information</strong>
                <small>Discover important findings</small>
              </div>
            </button>

            <button
              onClick={() =>
                setQuestion("Explain the main concepts in simple words.")
              }
            >
              <span>✧</span>
              <div>
                <strong>Explain a concept</strong>
                <small>Understand a topic more easily</small>
              </div>
            </button>

            <button
              onClick={() =>
                setQuestion("What conclusions does the document make?")
              }
            >
              <span>≡</span>
              <div>
                <strong>Explore conclusions</strong>
                <small>Review the document's takeaways</small>
              </div>
            </button>
          </div>
        </div>
      ) : (
        <div className="messages">
          {messages.map((message, index) => (
            <article
              className={`message ${message.role}`}
              key={`${index}-${message.role}`}
            >
              <div className="message-avatar">
                {message.role === "user"
                  ? "U"
                  : message.role === "error"
                    ? "!"
                    : "D"}
              </div>

              <div className="message-content">
                <div className="message-author">
                  {message.role === "user"
                    ? "You"
                    : message.role === "error"
                      ? "Connection issue"
                      : "DocuMind"}
                </div>
                <div className="message-text">{message.text}</div>

                {message.sources?.length > 0 && (
                  <div className="sources">
                    <h4>Retrieved sources ({message.sources.length})</h4>
                    {message.sources.map((source, sourceIndex) => (
                      <details
                        className="source-card"
                        key={`${source.name}-${source.chunk}-${sourceIndex}`}
                      >
                        <summary>
                          <span className="source-number">
                            {sourceIndex + 1}
                          </span>
                          <span className="source-name">
                            {source.name}
                            <small>Chunk {source.chunk}</small>
                          </span>
                          <span className="source-arrow">⌄</span>
                        </summary>
                        <p>{source.text}</p>
                      </details>
                    ))}
                  </div>
                )}
              </div>
            </article>
          ))}

          {loading && (
            <article className="message assistant">
              <div className="message-avatar">D</div>
              <div className="message-content">
                <div className="message-author">DocuMind</div>
                <div className="loading-indicator">
                  <span />
                  <span />
                  <span />
                  <small>Searching documents and generating an answer...</small>
                </div>
              </div>
            </article>
          )}
        </div>
      )}
    </section>

    <footer className="composer-area">
      {apiStatus === "offline" && (
        <p className="offline-notice">
          Start your FastAPI backend to ask questions.
        </p>
      )}

      <form className="composer" onSubmit={sendQuestion}>
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              sendQuestion(event);
            }
          }}
          placeholder="Ask a question about your documents..."
          rows={2}
          maxLength={4000}
          aria-label="Your question"
          disabled={loading}
        />
        <div className="composer-bottom">
          <span>Answers are grounded in your indexed documents.</span>
          <button
            className="send-button"
            type="submit"
            disabled={!question.trim() || loading}
            aria-label="Send question"
          >
            {loading ? "..." : "↑"}
          </button>
        </div>
      </form>
      <p className="footer-note">
        AI-generated responses can be inaccurate. Verify important details
        against the original documents.
      </p>
    </footer>
  </main>
</div>


);
}

export default App;
