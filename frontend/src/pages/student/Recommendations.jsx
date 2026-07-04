import React, { useState, useEffect } from "react";
import Header from "../../components/Header";
import API from "../../services/api";

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedRec, setSelectedRec] = useState(null);
  
  // Stages tracking for friendly spinner/progress
  const [stage, setStage] = useState("Extracting resume text...");

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      setError("");
      setStage("Reading resume credentials...");
      
      const timer1 = setTimeout(() => setStage("Normalizing skills and education..."), 1000);
      const timer2 = setTimeout(() => setStage("Generating sentence embedding..."), 2000);
      const timer3 = setTimeout(() => setStage("Calculating semantic similarity matches..."), 3000);
      const timer4 = setTimeout(() => setStage("Ranking using business eligibility rules..."), 4000);
      
      const res = await API.get("/recommendations");
      
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
      clearTimeout(timer4);

      if (res.data.success) {
        setRecommendations(res.data.data || []);
      } else {
        setError(res.data.message || "Failed to generate recommendations");
      }
    } catch (err) {
      setError(
        err.response?.data?.message || 
        "Failed to load recommendations. Please verify the AI Service is running."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  return (
    <div style={styles.page}>
      <Header />
      <main style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>AI Internship Recommendations</h1>
          <p style={styles.subtitle}>Factual, semantic matches scored using SpaCy NLP and sentence-transformers.</p>
        </div>

        {error && (
          <div style={styles.errorContainer}>
            <p style={styles.errorText}>{error}</p>
            <button onClick={fetchRecommendations} style={styles.retryBtn}>Retry Match</button>
          </div>
        )}

        {loading ? (
          <div style={styles.loaderContainer}>
            <div style={styles.spinner}></div>
            <p style={styles.loaderText}>{stage}</p>
            <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
          </div>
        ) : (
          !error && (
            <div style={styles.content}>
              {recommendations.length === 0 ? (
                <div style={styles.emptyState}>
                  <p>No internships found matching your skills profile.</p>
                </div>
              ) : (
                <div style={styles.grid}>
                  {recommendations.map((rec) => (
                    <div key={rec.internship_id} style={styles.card} onClick={() => setSelectedRec(rec)}>
                      <div style={styles.cardHeader}>
                        <span style={styles.matchBadge}>{Math.round(rec.final_score * 100)}% Match</span>
                      </div>
                      <h3 style={styles.cardTitle}>{rec.title}</h3>
                      <p style={styles.companyName}>{rec.company}</p>
                      <div style={styles.cardMeta}>
                        <span style={styles.metaItem}>📍 {rec.location || "Remote"}</span>
                        <span style={styles.metaItem}>💼 {rec.mode || "ONLINE"}</span>
                      </div>
                      <button style={styles.viewBtn}>View Match Details</button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        )}

        {/* DETAILS OVERLAY MODAL */}
        {selectedRec && (
          <div style={styles.modalOverlay} onClick={() => setSelectedRec(null)}>
            <div style={styles.modalContent} onClick={(e) => e.stopPropagation()}>
              <div style={styles.modalHeader}>
                <div>
                  <span style={styles.modalMatchBadge}>{Math.round(selectedRec.final_score * 100)}% Match Score</span>
                  <h2 style={styles.modalTitle}>{selectedRec.title}</h2>
                  <p style={styles.modalCompany}>{selectedRec.company} — {selectedRec.location || "Remote"} ({selectedRec.mode})</p>
                </div>
                <button style={styles.closeBtn} onClick={() => setSelectedRec(null)}>×</button>
              </div>

              <div style={styles.modalBody}>
                {/* Score explanation text */}
                <div style={styles.section}>
                  <h4 style={styles.sectionLabel}>Semantic Match Explanation</h4>
                  <p style={styles.explanationText}>{selectedRec.explanation_text}</p>
                </div>

                {/* Score breakdown bars */}
                <div style={styles.section}>
                  <h4 style={styles.sectionLabel}>Composite Score Breakdown</h4>
                  <div style={styles.breakdownGroup}>
                    <div style={styles.breakdownRow}>
                      <span style={styles.breakdownName}>Semantic Similarity (45%)</span>
                      <div style={styles.barBg}><div style={{ ...styles.barFill, width: `${selectedRec.score_breakdown.semantic_similarity * 100}%`, backgroundColor: "#4f46e5" }}></div></div>
                      <span style={styles.breakdownVal}>{Math.round(selectedRec.score_breakdown.semantic_similarity * 100)}%</span>
                    </div>
                    <div style={styles.breakdownRow}>
                      <span style={styles.breakdownName}>Skills Compatibility (25%)</span>
                      <div style={styles.barBg}><div style={{ ...styles.barFill, width: `${selectedRec.score_breakdown.skill_match * 100}%`, backgroundColor: "#10b981" }}></div></div>
                      <span style={styles.breakdownVal}>{Math.round(selectedRec.score_breakdown.skill_match * 100)}%</span>
                    </div>
                    <div style={styles.breakdownRow}>
                      <span style={styles.breakdownName}>Education Alignment (15%)</span>
                      <div style={styles.barBg}><div style={{ ...styles.barFill, width: `${selectedRec.score_breakdown.education_match * 100}%`, backgroundColor: "#f59e0b" }}></div></div>
                      <span style={styles.breakdownVal}>{Math.round(selectedRec.score_breakdown.education_match * 100)}%</span>
                    </div>
                    <div style={styles.breakdownRow}>
                      <span style={styles.breakdownName}>Experience Level (10%)</span>
                      <div style={styles.barBg}><div style={{ ...styles.barFill, width: `${selectedRec.score_breakdown.experience_match * 100}%`, backgroundColor: "#ec4899" }}></div></div>
                      <span style={styles.breakdownVal}>{Math.round(selectedRec.score_breakdown.experience_match * 100)}%</span>
                    </div>
                    <div style={styles.breakdownRow}>
                      <span style={styles.breakdownName}>Eligibility Rules (5%)</span>
                      <div style={styles.barBg}><div style={{ ...styles.barFill, width: `${selectedRec.score_breakdown.eligibility_match * 100}%`, backgroundColor: "#6b7280" }}></div></div>
                      <span style={styles.breakdownVal}>{Math.round(selectedRec.score_breakdown.eligibility_match * 100)}%</span>
                    </div>
                  </div>
                </div>

                {/* Skills details */}
                <div style={styles.section}>
                  <h4 style={styles.sectionLabel}>Skills Matching</h4>
                  <div style={styles.skillsLists}>
                    <div>
                      <span style={styles.subLabel}>Matched Skills ({selectedRec.matched_skills.length})</span>
                      <div style={styles.badgesWrap}>
                        {selectedRec.matched_skills.map(s => <span key={s} style={styles.greenBadge}>{s}</span>)}
                        {selectedRec.matched_skills.length === 0 && <span style={styles.emptyBadge}>None</span>}
                      </div>
                    </div>
                    <div style={{ marginTop: "1rem" }}>
                      <span style={styles.subLabel}>Missing Skills ({selectedRec.missing_skills.length})</span>
                      <div style={styles.badgesWrap}>
                        {selectedRec.missing_skills.map(s => <span key={s} style={styles.redBadge}>{s}</span>)}
                        {selectedRec.missing_skills.length === 0 && <span style={styles.emptyBadge}>None</span>}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Description and apply link */}
                <div style={styles.section}>
                  <h4 style={styles.sectionLabel}>Job Description</h4>
                  <p style={styles.descriptionText}>{selectedRec.description}</p>
                </div>

                {selectedRec.apply_url && (
                  <a href={selectedRec.apply_url} target="_blank" rel="noopener noreferrer" style={styles.applyBtn}>
                    Apply on Company Website ↗
                  </a>
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

const styles = {
  page: {
    backgroundColor: "#f9fafb",
    minHeight: "100vh",
    fontFamily: "Inter, -apple-system, sans-serif"
  },
  container: {
    maxWidth: 1200,
    margin: "0 auto",
    padding: "2rem 1.5rem"
  },
  header: {
    marginBottom: "2rem",
    textAlign: "center"
  },
  title: {
    fontSize: "1.75rem",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "0.5rem"
  },
  subtitle: {
    color: "#6b7280",
    fontSize: "1rem"
  },
  errorContainer: {
    textAlign: "center",
    padding: "2.5rem 1.5rem",
    backgroundColor: "#fef2f2",
    border: "1px solid #fee2e2",
    borderRadius: "0.75rem",
    maxWidth: 500,
    margin: "2rem auto"
  },
  errorText: {
    color: "#b91c1c",
    fontSize: "0.95rem",
    marginBottom: "1rem"
  },
  retryBtn: {
    backgroundColor: "#ef4444",
    color: "#ffffff",
    border: "none",
    padding: "0.5rem 1.25rem",
    borderRadius: "0.375rem",
    fontWeight: 500,
    cursor: "pointer"
  },
  loaderContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "4rem 0"
  },
  spinner: {
    width: 40,
    height: 40,
    border: "4px solid #4f46e5",
    borderTopColor: "transparent",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
    marginBottom: "1rem"
  },
  loaderText: {
    color: "#4b5563",
    fontSize: "1rem",
    fontWeight: 500
  },
  content: {},
  emptyState: {
    textAlign: "center",
    color: "#6b7280",
    padding: "3rem 0"
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
    gap: "1.5rem"
  },
  card: {
    backgroundColor: "#ffffff",
    padding: "1.5rem",
    borderRadius: "0.75rem",
    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
    border: "1px solid #e5e7eb",
    cursor: "pointer",
    display: "flex",
    flexDirection: "column",
    transition: "transform 0.2s, box-shadow 0.2s"
  },
  cardHeader: {
    marginBottom: "0.75rem"
  },
  matchBadge: {
    backgroundColor: "#eef2ff",
    color: "#4f46e5",
    padding: "0.25rem 0.5rem",
    borderRadius: "9999px",
    fontSize: "0.8rem",
    fontWeight: 600
  },
  cardTitle: {
    fontSize: "1.1rem",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "0.25rem",
    marginTop: 0
  },
  companyName: {
    color: "#4b5563",
    fontSize: "0.9rem",
    marginBottom: "1rem",
    marginTop: 0
  },
  cardMeta: {
    display: "flex",
    gap: "1rem",
    marginBottom: "1.25rem",
    marginTop: "auto"
  },
  metaItem: {
    fontSize: "0.8rem",
    color: "#6b7280",
    fontWeight: 500
  },
  viewBtn: {
    width: "100%",
    backgroundColor: "#f3f4f6",
    color: "#374151",
    border: "none",
    padding: "0.5rem",
    borderRadius: "0.375rem",
    fontSize: "0.9rem",
    fontWeight: 500,
    cursor: "pointer",
    transition: "background-color 0.2s"
  },
  modalOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(17, 24, 39, 0.6)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 100,
    padding: "1.5rem"
  },
  modalContent: {
    backgroundColor: "#ffffff",
    borderRadius: "0.75rem",
    width: "100%",
    maxWidth: 680,
    maxHeight: "85vh",
    display: "flex",
    flexDirection: "column",
    boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
  },
  modalHeader: {
    padding: "1.5rem",
    borderBottom: "1px solid #e5e7eb",
    display: "flex",
    justifyContent: "between",
    alignItems: "start"
  },
  modalMatchBadge: {
    backgroundColor: "#dcfce7",
    color: "#15803d",
    padding: "0.25rem 0.55rem",
    borderRadius: "9999px",
    fontSize: "0.8rem",
    fontWeight: 700,
    display: "inline-block",
    marginBottom: "0.5rem"
  },
  modalTitle: {
    fontSize: "1.4rem",
    fontWeight: "bold",
    color: "#111827",
    margin: 0
  },
  modalCompany: {
    color: "#4b5563",
    fontSize: "0.95rem",
    margin: "0.25rem 0 0 0"
  },
  closeBtn: {
    background: "none",
    border: "none",
    fontSize: "1.75rem",
    color: "#9ca3af",
    cursor: "pointer",
    lineHeight: 1,
    padding: 0,
    marginLeft: "auto"
  },
  modalBody: {
    padding: "1.5rem",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "1.5rem"
  },
  section: {
    borderBottom: "1px solid #f3f4f6",
    paddingBottom: "1rem"
  },
  sectionLabel: {
    fontSize: "0.9rem",
    fontWeight: 700,
    textTransform: "uppercase",
    color: "#374151",
    letterSpacing: "0.05em",
    marginTop: 0,
    marginBottom: "0.75rem"
  },
  explanationText: {
    color: "#4b5563",
    fontSize: "0.95rem",
    lineHeight: 1.5,
    margin: 0
  },
  breakdownGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "0.75rem"
  },
  breakdownRow: {
    display: "flex",
    alignItems: "center",
    gap: "1rem",
    fontSize: "0.85rem",
    color: "#4b5563"
  },
  breakdownName: {
    width: 200,
    fontWeight: 500
  },
  barBg: {
    flexGrow: 1,
    height: "0.5rem",
    backgroundColor: "#e5e7eb",
    borderRadius: "0.25rem",
    overflow: "hidden"
  },
  barFill: {
    height: "100%",
    borderRadius: "0.25rem"
  },
  breakdownVal: {
    width: 40,
    textAlign: "right",
    fontWeight: 600
  },
  subLabel: {
    fontSize: "0.85rem",
    fontWeight: 600,
    color: "#4b5563",
    display: "block",
    marginBottom: "0.5rem"
  },
  badgesWrap: {
    display: "flex",
    flexWrap: "wrap",
    gap: "0.5rem"
  },
  greenBadge: {
    backgroundColor: "#dcfce7",
    color: "#15803d",
    padding: "0.25rem 0.6rem",
    borderRadius: "0.375rem",
    fontSize: "0.8rem",
    fontWeight: 600
  },
  redBadge: {
    backgroundColor: "#fee2e2",
    color: "#b91c1c",
    padding: "0.25rem 0.6rem",
    borderRadius: "0.375rem",
    fontSize: "0.8rem",
    fontWeight: 600
  },
  emptyBadge: {
    color: "#9ca3af",
    fontSize: "0.85rem"
  },
  descriptionText: {
    color: "#4b5563",
    fontSize: "0.95rem",
    lineHeight: 1.6,
    margin: 0,
    whiteSpace: "pre-wrap"
  },
  applyBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    textDecoration: "none",
    textAlign: "center",
    padding: "0.75rem",
    borderRadius: "0.375rem",
    fontWeight: 600,
    fontSize: "1rem",
    transition: "background-color 0.2s"
  }
};

export default Recommendations;
