import React, { useState, useEffect } from "react";
import Header from "../../components/Header";
import API from "../../services/api";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Sparkles, 
  MapPin, 
  Briefcase, 
  ChevronRight, 
  X, 
  ArrowUpRight, 
  BarChart2, 
  CheckSquare, 
  AlertCircle,
  RefreshCw,
  BookOpen,
  Award
} from "lucide-react";

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
      if (err.response?.status === 404) {
        setError(err.response?.data?.message || "Please upload your resume first on the Dashboard to get personalized recommendations.");
      } else {
        setError(
          err.response?.data?.message || 
          "Failed to load recommendations. Please verify the AI Service is running."
        );
      }
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
        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          style={styles.header}
        >
          <div style={styles.headerBadge}>
            <Sparkles size={13} style={{ marginRight: 6, color: "#4f46e5" }} />
            AI recommendation Engine
          </div>
          <h1 style={styles.title}>Your Personalized Matchings</h1>
          <p style={styles.subtitle}>Factual, semantic matches scored in real-time using SpaCy NLP and SentenceTransformer representations.</p>
        </motion.div>

        {error && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            style={styles.errorContainer}
          >
            <AlertCircle size={36} style={{ color: "#ef4444", marginBottom: 12 }} />
            <p style={styles.errorText}>{error}</p>
            <button onClick={fetchRecommendations} style={styles.retryBtn}>
              <RefreshCw size={14} style={{ marginRight: 6 }} />
              Retry Match
            </button>
          </motion.div>
        )}

        {loading ? (
          <div style={styles.loaderContainer}>
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 1.2, ease: "linear" }}
              style={styles.spinner}
            />
            <motion.p 
              key={stage}
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              style={styles.loaderText}
            >
              {stage}
            </motion.p>
          </div>
        ) : (
          !error && (
            <div style={styles.content}>
              {recommendations.length === 0 ? (
                <motion.div 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  style={styles.emptyState}
                >
                  <p>No internships found matching your skills profile.</p>
                </motion.div>
              ) : (
                <div style={styles.grid}>
                  {recommendations.map((rec, index) => (
                    <motion.div 
                      key={rec.internship_id} 
                      initial={{ opacity: 0, y: 15 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.35, delay: index * 0.05 }}
                      whileHover={{ y: -4, boxShadow: "0 12px 20px -8px rgba(0,0,0,0.08), 0 4px 12px -2px rgba(0,0,0,0.03)" }}
                      style={styles.card} 
                      onClick={() => setSelectedRec(rec)}
                    >
                      <div style={styles.cardHeader}>
                        <span style={styles.matchBadge}>
                          <Sparkles size={11} style={{ marginRight: 4 }} />
                          {Math.round(rec.final_score * 100)}% Match
                        </span>
                      </div>
                      <h3 style={styles.cardTitle}>{rec.title}</h3>
                      <p style={styles.companyName}>{rec.company}</p>
                      
                      <div style={styles.cardMeta}>
                        <span style={styles.metaItem}>
                          <MapPin size={12} style={{ marginRight: 4, color: "#9ca3af" }} />
                          {rec.location || "Remote"}
                        </span>
                        <span style={styles.metaItem}>
                          <Briefcase size={12} style={{ marginRight: 4, color: "#9ca3af" }} />
                          {rec.mode || "ONLINE"}
                        </span>
                      </div>
                      
                      <button style={styles.viewBtn}>
                        View Details
                        <ChevronRight size={14} style={{ marginLeft: 4 }} />
                      </button>
                    </motion.div>
                  ))}
                </div>
              )}
            </div>
          )
        )}

        {/* DETAILS OVERLAY MODAL */}
        <AnimatePresence>
          {selectedRec && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              style={styles.modalOverlay} 
              onClick={() => setSelectedRec(null)}
            >
              <motion.div 
                initial={{ opacity: 0, scale: 0.95, y: 15 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 15 }}
                transition={{ type: "spring", damping: 25, stiffness: 350 }}
                style={styles.modalContent} 
                onClick={(e) => e.stopPropagation()}
              >
                <div style={styles.modalHeader}>
                  <div style={{ flexGrow: 1 }}>
                    <span style={styles.modalMatchBadge}>
                      <Sparkles size={12} style={{ marginRight: 4 }} />
                      {Math.round(selectedRec.final_score * 100)}% Match Score
                    </span>
                    <h2 style={styles.modalTitle}>{selectedRec.title}</h2>
                    <p style={styles.modalCompany}>{selectedRec.company} — {selectedRec.location || "Remote"} ({selectedRec.mode})</p>
                  </div>
                  <button style={styles.closeBtn} onClick={() => setSelectedRec(null)}>
                    <X size={20} />
                  </button>
                </div>

                <div style={styles.modalBody}>
                  {/* Score explanation text */}
                  <div style={styles.section}>
                    <h4 style={styles.sectionLabel}>
                      <Award size={14} style={{ marginRight: 6, color: "#4f46e5" }} />
                      Semantic Match Explanation
                    </h4>
                    <p style={styles.explanationText}>{selectedRec.explanation_text}</p>
                  </div>

                  {/* Score breakdown bars */}
                  <div style={styles.section}>
                    <h4 style={styles.sectionLabel}>
                      <BarChart2 size={14} style={{ marginRight: 6, color: "#4f46e5" }} />
                      Composite Score Breakdown
                    </h4>
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
                    <h4 style={styles.sectionLabel}>
                      <BookOpen size={14} style={{ marginRight: 6, color: "#4f46e5" }} />
                      Skills Compatibility Analysis
                    </h4>
                    <div style={styles.skillsLists}>
                      <div>
                        <span style={styles.subLabel}>Matched Skills ({selectedRec.matched_skills.length})</span>
                        <div style={styles.badgesWrap}>
                          {selectedRec.matched_skills.map(s => <span key={s} style={styles.greenBadge}>{s}</span>)}
                          {selectedRec.matched_skills.length === 0 && <span style={styles.emptyBadge}>None</span>}
                        </div>
                      </div>
                      <div style={{ marginTop: "1rem" }}>
                        <span style={styles.subLabel}>Missing / Recommended Skills ({selectedRec.missing_skills.length})</span>
                        <div style={styles.badgesWrap}>
                          {selectedRec.missing_skills.map(s => <span key={s} style={styles.redBadge}>{s}</span>)}
                          {selectedRec.missing_skills.length === 0 && <span style={styles.emptyBadge}>None</span>}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Description and apply link */}
                  <div style={styles.section}>
                    <h4 style={styles.sectionLabel}>
                      <CheckSquare size={14} style={{ marginRight: 6, color: "#4f46e5" }} />
                      Internship Description
                    </h4>
                    <p style={styles.descriptionText}>{selectedRec.description}</p>
                  </div>

                  {selectedRec.apply_url && (
                    <a href={selectedRec.apply_url} target="_blank" rel="noopener noreferrer" style={styles.applyBtn}>
                      Apply on Company Website
                      <ArrowUpRight size={16} style={{ marginLeft: 6 }} />
                    </a>
                  )}
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
};

const styles = {
  page: {
    background: "linear-gradient(180deg, #f9fafb 0%, #f3f4f6 100%)",
    minHeight: "100vh",
    fontFamily: "Inter, -apple-system, sans-serif"
  },
  container: {
    maxWidth: 1200,
    margin: "0 auto",
    padding: "3rem 1.5rem"
  },
  header: {
    marginBottom: "3rem",
    textAlign: "center",
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  headerBadge: {
    display: "inline-flex",
    alignItems: "center",
    backgroundColor: "#eef2ff",
    border: "1px solid #c7d2fe",
    borderRadius: "9999px",
    padding: "0.35rem 0.85rem",
    fontSize: "0.75rem",
    fontWeight: 600,
    color: "#4f46e5",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    marginBottom: "1rem"
  },
  title: {
    fontSize: "2.25rem",
    fontWeight: 800,
    color: "#111827",
    marginBottom: "0.75rem",
    letterSpacing: "-0.025em"
  },
  subtitle: {
    color: "#4b5563",
    fontSize: "1.05rem",
    maxWidth: 600,
    lineHeight: 1.5,
    margin: 0
  },
  errorContainer: {
    textAlign: "center",
    padding: "3rem 2rem",
    backgroundColor: "#ffffff",
    border: "1px solid #fee2e2",
    borderRadius: "1rem",
    boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.05)",
    maxWidth: 500,
    margin: "2rem auto",
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  errorText: {
    color: "#b91c1c",
    fontSize: "0.95rem",
    fontWeight: 500,
    marginBottom: "1.5rem",
    lineHeight: 1.5
  },
  retryBtn: {
    backgroundColor: "#ef4444",
    color: "#ffffff",
    border: "none",
    padding: "0.625rem 1.25rem",
    borderRadius: "0.5rem",
    fontWeight: 600,
    fontSize: "0.9rem",
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    boxShadow: "0 2px 4px rgba(239, 68, 68, 0.2)",
    transition: "background-color 0.2s"
  },
  loaderContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "6rem 0"
  },
  spinner: {
    width: 44,
    height: 44,
    border: "3px solid #e5e7eb",
    borderTopColor: "#4f46e5",
    borderRadius: "50%",
    marginBottom: "1.5rem"
  },
  loaderText: {
    color: "#4b5563",
    fontSize: "1.05rem",
    fontWeight: 600
  },
  content: {},
  emptyState: {
    textAlign: "center",
    color: "#6b7280",
    padding: "4rem 0"
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
    gap: "2rem"
  },
  card: {
    backgroundColor: "#ffffff",
    padding: "1.75rem",
    borderRadius: "1rem",
    boxShadow: "0 4px 6px -1px rgba(0,0,0,0.03), 0 2px 4px -1px rgba(0,0,0,0.02)",
    border: "1px solid rgba(229, 231, 235, 0.8)",
    cursor: "pointer",
    display: "flex",
    flexDirection: "column",
    position: "relative",
    overflow: "hidden"
  },
  cardHeader: {
    marginBottom: "1rem"
  },
  matchBadge: {
    display: "inline-flex",
    alignItems: "center",
    backgroundColor: "#eef2ff",
    color: "#4f46e5",
    padding: "0.3rem 0.65rem",
    borderRadius: "9999px",
    fontSize: "0.75rem",
    fontWeight: 700,
    border: "1px solid #e0e7ff"
  },
  cardTitle: {
    fontSize: "1.2rem",
    fontWeight: 700,
    color: "#111827",
    marginBottom: "0.35rem",
    marginTop: 0,
    lineHeight: 1.3
  },
  companyName: {
    color: "#4b5563",
    fontSize: "0.95rem",
    fontWeight: 500,
    marginBottom: "1.5rem",
    marginTop: 0
  },
  cardMeta: {
    display: "flex",
    gap: "1.25rem",
    marginBottom: "1.5rem",
    marginTop: "auto"
  },
  metaItem: {
    display: "flex",
    alignItems: "center",
    fontSize: "0.8rem",
    color: "#6b7280",
    fontWeight: 500
  },
  viewBtn: {
    width: "100%",
    backgroundColor: "#f9fafb",
    color: "#374151",
    border: "1px solid #e5e7eb",
    padding: "0.625rem",
    borderRadius: "0.5rem",
    fontSize: "0.875rem",
    fontWeight: 600,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    transition: "all 0.2s"
  },
  modalOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(17, 24, 39, 0.4)",
    backdropFilter: "blur(4px)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 100,
    padding: "1.5rem"
  },
  modalContent: {
    backgroundColor: "#ffffff",
    borderRadius: "1.25rem",
    width: "100%",
    maxWidth: 680,
    maxHeight: "85vh",
    display: "flex",
    flexDirection: "column",
    boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.15)",
    border: "1px solid rgba(229, 231, 235, 0.6)",
    overflow: "hidden"
  },
  modalHeader: {
    padding: "1.75rem 2rem",
    borderBottom: "1px solid #f3f4f6",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start"
  },
  modalMatchBadge: {
    display: "inline-flex",
    alignItems: "center",
    backgroundColor: "#dcfce7",
    color: "#15803d",
    padding: "0.3rem 0.75rem",
    borderRadius: "9999px",
    fontSize: "0.75rem",
    fontWeight: 700,
    marginBottom: "0.75rem",
    border: "1px solid #bbf7d0"
  },
  modalTitle: {
    fontSize: "1.5rem",
    fontWeight: 800,
    color: "#111827",
    margin: 0,
    letterSpacing: "-0.02em"
  },
  modalCompany: {
    color: "#4b5563",
    fontSize: "0.975rem",
    fontWeight: 500,
    margin: "0.35rem 0 0 0"
  },
  closeBtn: {
    background: "#f3f4f6",
    border: "none",
    borderRadius: "50%",
    width: 32,
    height: 32,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#6b7280",
    cursor: "pointer",
    padding: 0,
    marginLeft: "1.5rem",
    transition: "background-color 0.2s"
  },
  modalBody: {
    padding: "2rem",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "1.75rem"
  },
  section: {
    borderBottom: "1px solid #f3f4f6",
    paddingBottom: "1.5rem"
  },
  sectionLabel: {
    display: "flex",
    alignItems: "center",
    fontSize: "0.85rem",
    fontWeight: 700,
    textTransform: "uppercase",
    color: "#374151",
    letterSpacing: "0.05em",
    marginTop: 0,
    marginBottom: "1rem"
  },
  explanationText: {
    color: "#4b5563",
    fontSize: "0.95rem",
    lineHeight: 1.6,
    margin: 0
  },
  breakdownGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "0.85rem"
  },
  breakdownRow: {
    display: "flex",
    alignItems: "center",
    gap: "1.25rem",
    fontSize: "0.85rem",
    color: "#4b5563"
  },
  breakdownName: {
    width: 200,
    fontWeight: 600
  },
  barBg: {
    flexGrow: 1,
    height: "0.625rem",
    backgroundColor: "#f3f4f6",
    borderRadius: "9999px",
    overflow: "hidden"
  },
  barFill: {
    height: "100%",
    borderRadius: "9999px"
  },
  breakdownVal: {
    width: 40,
    textAlign: "right",
    fontWeight: 700
  },
  subLabel: {
    fontSize: "0.85rem",
    fontWeight: 600,
    color: "#374151",
    display: "block",
    marginBottom: "0.65rem"
  },
  badgesWrap: {
    display: "flex",
    flexWrap: "wrap",
    gap: "0.5rem"
  },
  greenBadge: {
    backgroundColor: "#dcfce7",
    color: "#15803d",
    border: "1px solid #bbf7d0",
    padding: "0.3rem 0.75rem",
    borderRadius: "0.5rem",
    fontSize: "0.8rem",
    fontWeight: 600
  },
  redBadge: {
    backgroundColor: "#fee2e2",
    color: "#b91c1c",
    border: "1px solid #fecaca",
    padding: "0.3rem 0.75rem",
    borderRadius: "0.5rem",
    fontSize: "0.8rem",
    fontWeight: 600
  },
  emptyBadge: {
    color: "#9ca3af",
    fontSize: "0.85rem",
    fontStyle: "italic"
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
    padding: "0.875rem",
    borderRadius: "0.5rem",
    fontWeight: 600,
    fontSize: "0.975rem",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow: "0 4px 6px -1px rgba(79, 70, 229, 0.2)",
    transition: "background-color 0.2s"
  }
};

export default Recommendations;
