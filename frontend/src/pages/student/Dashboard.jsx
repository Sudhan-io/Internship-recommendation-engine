import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import Header from "../../components/Header";
import API from "../../services/api";

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
        <div style={styles.welcomeCard}>
          <h1 style={styles.welcomeTitle}>Welcome Back, {user?.name}!</h1>
          <p style={styles.welcomeSubtitle}>Track your credentials and get instant internship matches.</p>
        </div>

        {loading ? (
          <div style={styles.loaderContainer}>
            <div style={styles.spinner}></div>
            <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
          </div>
        ) : (
          <div style={styles.grid}>
            {/* PROFILE CARD */}
            <div style={styles.card}>
              <h3 style={styles.cardTitle}>Student Profile</h3>
              <div style={styles.completeness}>
                <span style={styles.progressLabel}>Completeness: {getProfileCompleteness()}%</span>
                <div style={styles.progressBarBg}>
                  <div style={{ ...styles.progressBar, width: `${getProfileCompleteness()}%` }}></div>
                </div>
              </div>
              
              {profile ? (
                <div style={styles.profileDetails}>
                  <p style={styles.detailLine}><strong>College:</strong> {profile.collegeName}</p>
                  <p style={styles.detailLine}><strong>Department:</strong> {profile.department}</p>
                  <p style={styles.detailLine}><strong>CGPA:</strong> {profile.cgpa ? profile.cgpa.toFixed(2) : "N/A"}</p>
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
              <h3 style={styles.cardTitle}>Resume Details</h3>
              {resume ? (
                <div style={styles.resumeInfo}>
                  <div style={styles.resumeRow}>
                    <span style={styles.fileIcon}>📄</span>
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
                  {uploadError && <div style={styles.errorText}>{uploadError}</div>}
                  {uploadSuccess && <div style={styles.successText}>{uploadSuccess}</div>}
                  <label style={styles.uploadBtn}>
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
          </div>
        )}

        {/* QUICK RECOMMENDATIONS */}
        <div style={styles.recommendationQuickAction}>
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
          </button>
          {!resume && <p style={styles.hintText}>* You must upload a resume before you can generate matches.</p>}
        </div>
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
    padding: "2rem 1.5rem",
    display: "flex",
    flexDirection: "column",
    gap: "2rem"
  },
  welcomeCard: {
    backgroundColor: "#ffffff",
    padding: "2rem",
    borderRadius: "0.75rem",
    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
    border: "1px solid #e5e7eb"
  },
  welcomeTitle: {
    fontSize: "2rem",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "0.5rem"
  },
  welcomeSubtitle: {
    color: "#4b5563",
    fontSize: "1.05rem"
  },
  loaderContainer: {
    display: "flex",
    justifyContent: "center",
    padding: "3rem 0"
  },
  spinner: {
    width: 32,
    height: 32,
    border: "3px solid #4f46e5",
    borderTopColor: "transparent",
    borderRadius: "50%",
    animation: "spin 1s linear infinite"
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
    gap: "1.5rem"
  },
  card: {
    backgroundColor: "#ffffff",
    padding: "1.75rem",
    borderRadius: "0.75rem",
    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
    border: "1px solid #e5e7eb",
    display: "flex",
    flexDirection: "column"
  },
  cardTitle: {
    fontSize: "1.2rem",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "1rem"
  },
  completeness: {
    marginBottom: "1.25rem"
  },
  progressLabel: {
    fontSize: "0.85rem",
    fontWeight: 500,
    color: "#4b5563"
  },
  progressBarBg: {
    height: "0.5rem",
    backgroundColor: "#e5e7eb",
    borderRadius: "0.25rem",
    marginTop: "0.25rem",
    overflow: "hidden"
  },
  progressBar: {
    height: "100%",
    backgroundColor: "#4f46e5",
    borderRadius: "0.25rem",
    transition: "width 0.4s ease"
  },
  profileDetails: {
    display: "flex",
    flexDirection: "column",
    gap: "0.75rem"
  },
  detailLine: {
    fontSize: "0.95rem",
    color: "#374151",
    margin: 0
  },
  cardLink: {
    color: "#4f46e5",
    fontSize: "0.9rem",
    fontWeight: 500,
    textDecoration: "none",
    marginTop: "1rem",
    display: "inline-block"
  },
  emptyState: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    flexGrow: 1,
    textAlign: "center",
    padding: "1rem 0"
  },
  emptyText: {
    fontSize: "0.95rem",
    color: "#6b7280",
    marginBottom: "1.25rem"
  },
  actionBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    padding: "0.5rem 1rem",
    borderRadius: "0.375rem",
    fontSize: "0.9rem",
    fontWeight: 500,
    textDecoration: "none",
    transition: "background-color 0.2s"
  },
  uploadBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    padding: "0.5rem 1.25rem",
    borderRadius: "0.375rem",
    fontSize: "0.9rem",
    fontWeight: 500,
    cursor: "pointer",
    transition: "background-color 0.2s"
  },
  resumeInfo: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem"
  },
  resumeRow: {
    display: "flex",
    alignItems: "center",
    gap: "0.75rem",
    backgroundColor: "#f9fafb",
    padding: "0.75rem 1rem",
    borderRadius: "0.5rem",
    border: "1px dashed #d1d5db"
  },
  fileIcon: {
    fontSize: "1.5rem"
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
    color: "#6b7280"
  },
  statusLine: {
    fontSize: "0.9rem",
    color: "#4b5563",
    margin: 0
  },
  badge: {
    padding: "0.125rem 0.5rem",
    borderRadius: "9999px",
    fontSize: "0.8rem",
    fontWeight: 600,
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
    fontWeight: 500,
    cursor: "pointer",
    textDecoration: "underline"
  },
  errorText: {
    color: "#dc2626",
    fontSize: "0.85rem",
    marginBottom: "0.5rem"
  },
  successText: {
    color: "#16a34a",
    fontSize: "0.85rem",
    marginBottom: "0.5rem"
  },
  recommendationQuickAction: {
    backgroundColor: "#ffffff",
    padding: "2.5rem 2rem",
    borderRadius: "0.75rem",
    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
    border: "1px solid #e5e7eb",
    textAlign: "center",
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  sectionTitle: {
    fontSize: "1.5rem",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "0.5rem"
  },
  sectionDesc: {
    color: "#4b5563",
    maxWidth: 600,
    fontSize: "1rem",
    marginBottom: "1.5rem"
  },
  matchBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    border: "none",
    padding: "0.75rem 2rem",
    fontSize: "1rem",
    fontWeight: 600,
    borderRadius: "0.375rem",
    cursor: "pointer",
    transition: "background-color 0.2s"
  },
  matchBtnDisabled: {
    backgroundColor: "#9ca3af",
    cursor: "not-allowed"
  },
  hintText: {
    fontSize: "0.8rem",
    color: "#9ca3af",
    marginTop: "0.5rem"
  }
};

export default Dashboard;
