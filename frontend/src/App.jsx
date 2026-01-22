import { useEffect, useState } from "react";

const API_URL = "http://localhost:8000/news";

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cached, setCached] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(API_URL)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch news");
        }
        return res.json();
      })
      .then((data) => {
        setArticles(data.articles);
        setCached(data.cached);
        setLoading(false);
      })
      .catch(() => {
        setError("Could not load news.");
        setLoading(false);
      });
  }, []);

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🔥 Hottest Tech News</h1>

      {loading && <p>Loading summaries...</p>}
      {error && <p style={styles.error}>{error}</p>}

      {!loading && !error && (
        <>
          <p style={styles.subtext}>
            Source: Hacker News {cached && "(cached today)"}
          </p>

          {articles.map((article, idx) => (
            <div key={idx} style={styles.card}>
              <h2 style={styles.cardTitle}>{article.title}</h2>
              <pre style={styles.summary}>{article.summary}</pre>
              <a
                href={article.url}
                target="_blank"
                rel="noreferrer"
                style={styles.link}
              >
                Read full article →
              </a>
            </div>
          ))}
        </>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "800px",
    margin: "40px auto",
    fontFamily: "Arial, sans-serif",
    padding: "0 16px"
  },
  title: {
    textAlign: "center"
  },
  subtext: {
    textAlign: "center",
    color: "#666"
  },
  card: {
    border: "1px solid #ddd",
    borderRadius: "6px",
    padding: "16px",
    marginBottom: "20px"
  },
  cardTitle: {
    marginBottom: "10px"
  },
  summary: {
    whiteSpace: "pre-wrap",
    fontSize: "14px",
    marginBottom: "10px"
  },
  link: {
    textDecoration: "none",
    color: "#0070f3"
  },
  error: {
    color: "red",
    textAlign: "center"
  }
};

export default App;
