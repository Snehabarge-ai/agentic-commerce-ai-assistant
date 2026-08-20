import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

function Card({ p, featured }) {
  return (
    <div className={featured ? "card featured" : "card"}>
      {featured && <b className="badge">AI Recommendation</b>}

      <h3>{p.name}</h3>
      <small>{p.category}</small>

      <h2>₹{p.price.toLocaleString("en-IN")}</h2>

      <p>⭐ {p.rating}/5</p>

      <p>{p.features.join(" · ")}</p>
    </div>
  );
}

function App() {
  const [q, setQ] = useState("");
  const [r, setR] = useState(null);
  const [loading, setLoading] = useState(false);

  async function go(e) {
    e.preventDefault();

    if (!q.trim()) return;

    setLoading(true);

    try {
      const x = await fetch("https://agentic-commerce-ai-assistant-1.onrender.com", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: q,
        }),
      });

      const data = await x.json();
      setR(data);
    } catch (error) {
      console.error("API Error:", error);
      alert("Backend is not running. Please start Uvicorn.");
    }

    setLoading(false);
  }

  return (
    <main>
      <section className="hero">
        <small>AI-POWERED COMMERCE</small>

        <h1>Shop smarter with an AI agent.</h1>

        <p>
          Describe what you need. The agent extracts intent, searches
          products, ranks options and explains the recommendation.
        </p>

        <form onSubmit={go}>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="wireless headphones under 5000 for travel"
          />

          <button>
            {loading ? "Thinking..." : "Find Products"}
          </button>
        </form>
      </section>

      {r && (
        <section>
          {/* Agent Pipeline */}
          <div className="panel">
            <h2>Agent pipeline</h2>

            {r.agent_steps.map((s, i) => (
              <span className="step" key={s}>
                {i + 1}. {s}
              </span>
            ))}
          </div>

          {/* Best Recommendation */}
          <Card p={r.recommendation} featured />

          {/* AI Explanation */}
          {r.ai_explanation && (
            <div className="ai-explanation">
              <h2>🤖 Why this product?</h2>

              <p>{r.ai_explanation}</p>
            </div>
          )}

          {/* Alternatives */}
          <h2>Alternatives</h2>

          <div className="grid">
            {r.alternatives.map((p) => (
              <Card p={p} key={p.id} />
            ))}
          </div>
        </section>
      )}
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);