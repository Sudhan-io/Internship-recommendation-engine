import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import Header from "../../components/Header";
import API from "../../services/api";
import { motion } from "framer-motion";
import { 
  User, 
  FileText, 
  CheckCircle2, 
  AlertCircle, 
  ArrowRight, 
  UploadCloud, 
  GraduationCap, 
  Building2 
} from "lucide-react";

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const [uploadSuccess, setUploadSuccess] = useState("");
  
  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      setLoading(true);
      // Fetch profile
      const profRes = await API.get("/student/profile");
      if (profRes.data.success) {
        setProfile(profRes.data.data);
      }
      
      // Fetch resume
      const resRes = await API.get("/resumes/my-resume");
      if (resRes.data.success) {
        setResume(resRes.data.data);
      }
    } catch (err) {
      console.log("Could not load dashboard data: ", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
      setUploadError("Only PDF files are allowed");
      return;
    }

    setUploading(true);
    setUploadError("");
    setUploadSuccess("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await API.post("/resumes/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      if (res.data.success) {
        setUploadSuccess("Resume uploaded and processed successfully!");
        setResume(res.data.data);
      } else {
        setUploadError(res.data.message || "Failed to process resume");
      }
    } catch (err) {
      setUploadError(err.response?.data?.message || "Error uploading resume");
    } finally {
      setUploading(false);
    }
  };

  const getProfileCompleteness = () => {
    if (!profile) return 0;
    let score = 0;
    if (profile.collegeName) score += 20;
    if (profile.department) score += 20;
    if (profile.yearOfStudy) score += 20;
    if (profile.cgpa) score += 20;
    if (profile.phone) score += 20;
    return score;
  };

  return (
    <div style={styles.page}>
      <Header />
      <main style={styles.container}>
        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          style={styles.welcomeCard}
        >
          <h1 style={styles.welcomeTitle}>Welcome Back, {user?.name}!</h1>
          <p style={styles.welcomeSubtitle}>Track your credentials and get instant internship matches.</p>
        </motion.div>

        {loading ? (
          <div style={styles.loaderContainer}>
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 1.2, ease: "linear" }}
              style={styles.spinner}
            />
          </div>
        ) : (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.1, duration: 0.4 }}
            style={styles.grid}
          >
            {/* PROFILE CARD */}
            <div style={styles.card}>
              <div style={styles.cardHeaderRow}>
                <User size={18} style={{ color: "#4f46e5" }} />
                <h3 style={styles.cardTitle}>Student Profile</h3>
              </div>
              <div style={styles.completeness}>
                <span style={styles.progressLabel}>Completeness: {getProfileCompleteness()}%</span>
                <div style={styles.progressBarBg}>
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: `${getProfileCompleteness()}%` }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    style={styles.progressBar}
                  />
                </div>
              </div>
              
              {profile ? (
                <div style={styles.profileDetails}>
                  <p style={styles.detailLine}>
                    <Building2 size={13} style={styles.detailIcon} />
                    <strong>College:</strong> {profile.collegeName}
                  </p>
                  <p style={styles.detailLine}>
                    <GraduationCap size={13} style={styles.detailIcon} />
                    <strong>Department:</strong> {profile.department}
                  </p>
                  <p style={styles.detailLine}>
                    <CheckCircle2 size={13} style={styles.detailIcon} />
                    <strong>CGPA:</strong> {profile.cgpa ? profile.cgpa.toFixed(2) : "N/A"}
                  </p>
                  <Link to="/profile" style={styles.cardLink}>Update Profile</Link>
                </div>
              ) : (
                <div style={styles.emptyState}>
                  <p style={styles.emptyText}>You haven't completed your profile details yet.</p>
                  <Link to="/profile" style={styles.actionBtn}>Complete Profile</Link>
                </div>
              )}
            </div>

            {/* RESUME CARD */}
            <div style={styles.card}>
              <div style={styles.cardHeaderRow}>
                <FileText size={18} style={{ color: "#4f46e5" }} />
                <h3 style={styles.cardTitle}>Resume Details</h3>
              </div>
              {resume ? (
                <div style={styles.resumeInfo}>
                  <div style={styles.resumeRow}>
                    <FileText size={24} style={{ color: "#4f46e5", flexShrink: 0 }} />
                    <div style={styles.fileMeta}>
                      <span style={styles.fileName}>{resume.fileName}</span>
                      <span style={styles.fileSize}>{(resume.fileSize / 1024).toFixed(1)} KB</span>
                    </div>
                  </div>
                  <p style={styles.statusLine}>
                    <strong>Status:</strong>{" "}
                    <span style={{
                      ...styles.badge,
                      ...(resume.processingStatus === "TEXT_EXTRACTED" ? styles.badgeSuccess : {})
                    }}>
                      {resume.processingStatus}
                    </span>
                  </p>
                  <div style={styles.reuploadGroup}>
                    <label style={styles.reuploadLabel}>
                      {uploading ? "Uploading..." : "Upload New Resume"}
                      <input
                        type="file"
                        accept=".pdf"
                        onChange={handleFileUpload}
                        disabled={uploading}
                        style={{ display: "none" }}
                      />
                    </label>
                  </div>
                </div>
              ) : (
                <div style={styles.emptyState}>
                  <p style={styles.emptyText}>Please upload your resume in PDF format to parse skills.</p>
                  {uploadError && <div style={styles.errorText}><AlertCircle size={12} style={{ marginRight: 4 }} />{uploadError}</div>}
                  {uploadSuccess && <div style={styles.successText}><CheckCircle2 size={12} style={{ marginRight: 4 }} />{uploadSuccess}</div>}
                  <label style={styles.uploadBtn}>
                    <UploadCloud size={14} style={{ marginRight: 6 }} />
                    {uploading ? "Processing PDF..." : "Upload Resume"}
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handleFileUpload}
                      disabled={uploading}
                      style={{ display: "none" }}
                    />
                  </label>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {/* QUICK RECOMMENDATIONS */}
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.4 }}
          style={styles.recommendationQuickAction}
        >
          <h2 style={styles.sectionTitle}>Get AI Internship Recommendations</h2>
          <p style={styles.sectionDesc}>Our NLP matching engine will score and rank internships based on your resume skills and college qualifications.</p>
          <button
            onClick={() => navigate("/recommendations")}
            disabled={!resume}
            style={{
              ...styles.matchBtn,
              ...(!resume ? styles.matchBtnDisabled : {})
            }}
          >
            Find Matches Now
            <ArrowRight size={16} style={{ marginLeft: 6 }} />
          </button>
          {!resume && <p style={styles.hintText}>* You must upload a resume before you can generate matches.</p>}
        </motion.div>
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
    padding: "3rem 1.5rem",
    display: "flex",
    flexDirection: "column",
    gap: "2.5rem"
  },
  welcomeCard: {
    backgroundColor: "#ffffff",
    padding: "2.5rem",
    borderRadius: "1rem",
    boxShadow: "0 4px 6px -1px rgba(0,0,0,0.03), 0 2px 4px -1px rgba(0,0,0,0.02)",
    border: "1px solid rgba(229, 231, 235, 0.8)"
  },
  welcomeTitle: {
    fontSize: "2rem",
    fontWeight: 800,
    color: "#111827",
    marginBottom: "0.5rem",
    letterSpacing: "-0.02em"
  },
  welcomeSubtitle: {
    color: "#4b5563",
    fontSize: "1.05rem"
  },
  loaderContainer: {
    display: "flex",
    justifyContent: "center",
    padding: "4rem 0"
  },
  spinner: {
    width: 36,
    height: 36,
    border: "3px solid #e5e7eb",
    borderTopColor: "#4f46e5",
    borderRadius: "50%",
    animation: "spin 1s linear infinite"
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
    gap: "2rem"
  },
  card: {
    backgroundColor: "#ffffff",
    padding: "2rem",
    borderRadius: "1rem",
    boxShadow: "0 4px 6px -1px rgba(0,0,0,0.03), 0 2px 4px -1px rgba(0,0,0,0.02)",
    border: "1px solid rgba(229, 231, 235, 0.8)",
    display: "flex",
    flexDirection: "column"
  },
  cardHeaderRow: {
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
    marginBottom: "1.25rem"
  },
  cardTitle: {
    fontSize: "1.2rem",
    fontWeight: 700,
    color: "#111827",
    margin: 0
  },
  completeness: {
    marginBottom: "1.5rem"
  },
  progressLabel: {
    fontSize: "0.85rem",
    fontWeight: 600,
    color: "#4b5563"
  },
  progressBarBg: {
    height: "0.5rem",
    backgroundColor: "#f3f4f6",
    borderRadius: "9999px",
    marginTop: "0.5rem",
    overflow: "hidden"
  },
  progressBar: {
    height: "100%",
    backgroundColor: "#4f46e5",
    borderRadius: "9999px"
  },
  profileDetails: {
    display: "flex",
    flexDirection: "column",
    gap: "0.85rem"
  },
  detailLine: {
    display: "flex",
    alignItems: "center",
    fontSize: "0.95rem",
    color: "#374151",
    margin: 0
  },
  detailIcon: {
    marginRight: 8,
    color: "#9ca3af"
  },
  cardLink: {
    color: "#4f46e5",
    fontSize: "0.9rem",
    fontWeight: 600,
    textDecoration: "none",
    marginTop: "1.25rem",
    display: "inline-block"
  },
  emptyState: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    flexGrow: 1,
    textAlign: "center",
    padding: "1.5rem 0"
  },
  emptyText: {
    fontSize: "0.95rem",
    color: "#6b7280",
    marginBottom: "1.5rem"
  },
  actionBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    padding: "0.625rem 1.25rem",
    borderRadius: "0.5rem",
    fontSize: "0.9rem",
    fontWeight: 600,
    textDecoration: "none",
    boxShadow: "0 2px 4px rgba(79, 70, 229, 0.15)",
    transition: "background-color 0.2s"
  },
  uploadBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    padding: "0.625rem 1.25rem",
    borderRadius: "0.5rem",
    fontSize: "0.9rem",
    fontWeight: 600,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    boxShadow: "0 2px 4px rgba(79, 70, 229, 0.15)",
    transition: "background-color 0.2s"
  },
  resumeInfo: {
    display: "flex",
    flexDirection: "column",
    gap: "1.25rem"
  },
  resumeRow: {
    display: "flex",
    alignItems: "center",
    gap: "0.85rem",
    backgroundColor: "#f9fafb",
    padding: "1rem",
    borderRadius: "0.75rem",
    border: "1px dashed #d1d5db"
  },
  fileMeta: {
    display: "flex",
    flexDirection: "column",
    overflow: "hidden"
  },
  fileName: {
    fontSize: "0.9rem",
    fontWeight: 600,
    color: "#374151",
    whiteSpace: "nowrap",
    textOverflow: "ellipsis",
    overflow: "hidden"
  },
  fileSize: {
    fontSize: "0.8rem",
    color: "#6b7280",
    marginTop: "0.125rem"
  },
  statusLine: {
    fontSize: "0.9rem",
    color: "#4b5563",
    margin: 0
  },
  badge: {
    padding: "0.25rem 0.65rem",
    borderRadius: "9999px",
    fontSize: "0.75rem",
    fontWeight: 700,
    backgroundColor: "#f3f4f6",
    color: "#374151"
  },
  badgeSuccess: {
    backgroundColor: "#dcfce7",
    color: "#15803d"
  },
  reuploadGroup: {
    marginTop: "0.5rem"
  },
  reuploadLabel: {
    color: "#4f46e5",
    fontSize: "0.9rem",
    fontWeight: 600,
    cursor: "pointer",
    textDecoration: "underline"
  },
  errorText: {
    color: "#dc2626",
    fontSize: "0.85rem",
    fontWeight: 500,
    marginBottom: "0.75rem",
    display: "flex",
    alignItems: "center"
  },
  successText: {
    color: "#16a34a",
    fontSize: "0.85rem",
    fontWeight: 500,
    marginBottom: "0.75rem",
    display: "flex",
    alignItems: "center"
  },
  recommendationQuickAction: {
    backgroundColor: "#ffffff",
    padding: "3rem 2rem",
    borderRadius: "1rem",
    boxShadow: "0 4px 6px -1px rgba(0,0,0,0.03), 0 2px 4px -1px rgba(0,0,0,0.02)",
    border: "1px solid rgba(229, 231, 235, 0.8)",
    textAlign: "center",
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  sectionTitle: {
    fontSize: "1.5rem",
    fontWeight: 800,
    color: "#111827",
    marginBottom: "0.5rem",
    letterSpacing: "-0.02em"
  },
  sectionDesc: {
    color: "#4b5563",
    maxWidth: 600,
    fontSize: "1rem",
    marginBottom: "1.75rem",
    lineHeight: 1.5
  },
  matchBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    border: "none",
    padding: "0.75rem 2rem",
    fontSize: "1rem",
    fontWeight: 600,
    borderRadius: "0.5rem",
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    boxShadow: "0 4px 6px -1px rgba(79, 70, 229, 0.2)",
    transition: "background-color 0.2s"
  },
  matchBtnDisabled: {
    backgroundColor: "#9ca3af",
    cursor: "not-allowed",
    boxShadow: "none"
  },
  hintText: {
    fontSize: "0.8rem",
    color: "#9ca3af",
    marginTop: "0.75rem"
  }
};

export default Dashboard;
