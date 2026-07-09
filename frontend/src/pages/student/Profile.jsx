import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../../components/Header";
import API from "../../services/api";
import { motion } from "framer-motion";
import { 
  GraduationCap, 
  BookOpen, 
  Phone, 
  Save, 
  AlertCircle, 
  CheckCircle2,
  Calendar,
  Award
} from "lucide-react";

// Inline SVG components to bypass lucide-react brand icon version restrictions
const GithubIcon = ({ size = 13, style }) => (
  <svg 
    viewBox="0 0 24 24" 
    width={size} 
    height={size} 
    stroke="currentColor" 
    strokeWidth="2" 
    fill="none" 
    strokeLinecap="round" 
    strokeLinejoin="round" 
    style={style}
  >
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
    <path d="M9 18c-4.51 2-5-2-7-2" />
  </svg>
);

const LinkedinIcon = ({ size = 13, style }) => (
  <svg 
    viewBox="0 0 24 24" 
    width={size} 
    height={size} 
    stroke="currentColor" 
    strokeWidth="2" 
    fill="none" 
    strokeLinecap="round" 
    strokeLinejoin="round" 
    style={style}
  >
    <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z" />
    <rect x="2" y="9" width="4" height="12" />
    <circle cx="4" cy="4" r="2" />
  </svg>
);

const Profile = () => {
  const [collegeName, setCollegeName] = useState("");
  const [department, setDepartment] = useState("");
  const [yearOfStudy, setYearOfStudy] = useState(1);
  const [cgpa, setCgpa] = useState("");
  const [phone, setPhone] = useState("");
  const [linkedinUrl, setLinkedinUrl] = useState("");
  const [githubUrl, setGithubUrl] = useState("");
  
  const [hasProfile, setHasProfile] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(true);
        const res = await API.get("/student/profile");
        if (res.data.success && res.data.data) {
          const profile = res.data.data;
          setCollegeName(profile.collegeName || "");
          setDepartment(profile.department || "");
          setYearOfStudy(profile.yearOfStudy || 1);
          setCgpa(profile.cgpa ? String(profile.cgpa) : "");
          setPhone(profile.phone || "");
          setLinkedinUrl(profile.linkedinUrl || "");
          setGithubUrl(profile.githubUrl || "");
          setHasProfile(true);
        }
      } catch (err) {
        console.log("No profile loaded or user is unregistered.");
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const validateForm = () => {
    if (!collegeName.trim()) return "College name is required";
    if (!department.trim()) return "Department is required";
    
    const cgpaNum = parseFloat(cgpa);
    if (isNaN(cgpaNum) || cgpaNum < 0 || cgpaNum > 10) {
      return "CGPA must be a valid number between 0.0 and 10.0";
    }

    const phoneRegex = /^\d{10,12}$/;
    if (phone && !phoneRegex.test(phone)) {
      return "Phone number must be between 10 and 12 digits";
    }

    const urlRegex = /^(https?:\/\/)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(\/\S*)?$/;
    if (linkedinUrl && !urlRegex.test(linkedinUrl)) {
      return "Invalid LinkedIn Profile URL";
    }
    if (githubUrl && !urlRegex.test(githubUrl)) {
      return "Invalid GitHub Profile URL";
    }

    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    setSaving(true);
    const payload = {
      collegeName,
      department,
      yearOfStudy: parseInt(yearOfStudy),
      cgpa: parseFloat(cgpa),
      phone,
      linkedinUrl,
      githubUrl
    };

    try {
      let res;
      if (hasProfile) {
        res = await API.put("/student/profile", payload);
      } else {
        res = await API.post("/student/profile", payload);
      }

      if (res.data.success) {
        setSuccess("Profile details saved successfully!");
        setHasProfile(true);
        setTimeout(() => navigate("/dashboard"), 1500);
      } else {
        setError(res.data.message || "Failed to save profile");
      }
    } catch (err) {
      setError(err.response?.data?.message || "An error occurred while saving profile");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={styles.page}>
      <Header />
      <main style={styles.container}>
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          style={styles.card}
        >
          <div style={styles.header}>
            <h2 style={styles.title}>Student Profile Setup</h2>
            <p style={styles.subtitle}>Provide your academic details and social profiles to optimize recommendation matching.</p>
          </div>

          {loading ? (
            <div style={styles.loaderContainer}>
              <motion.div 
                animate={{ rotate: 360 }}
                transition={{ repeat: Infinity, duration: 1.2, ease: "linear" }}
                style={styles.spinner}
              />
            </div>
          ) : (
            <form onSubmit={handleSubmit} style={styles.form}>
              {error && (
                <div style={styles.errorAlert}>
                  <AlertCircle size={16} style={{ marginRight: 8, flexShrink: 0 }} />
                  {error}
                </div>
              )}
              {success && (
                <div style={styles.successAlert}>
                  <CheckCircle2 size={16} style={{ marginRight: 8, flexShrink: 0 }} />
                  {success}
                </div>
              )}

              <div style={styles.row}>
                <div style={styles.inputGroup}>
                  <label style={styles.label}>
                    <GraduationCap size={13} style={styles.fieldIcon} />
                    College/University Name
                  </label>
                  <input
                    type="text"
                    required
                    value={collegeName}
                    onChange={(e) => setCollegeName(e.target.value)}
                    style={styles.input}
                    placeholder="Stanford University"
                  />
                </div>
                
                <div style={styles.inputGroup}>
                  <label style={styles.label}>
                    <BookOpen size={13} style={styles.fieldIcon} />
                    Department/Major
                  </label>
                  <input
                    type="text"
                    required
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    style={styles.input}
                    placeholder="Computer Science & Engineering"
                  />
                </div>
              </div>

              <div style={styles.row}>
                <div style={styles.inputGroup}>
                  <label style={styles.label}>
                    <Calendar size={13} style={styles.fieldIcon} />
                    Year of Study
                  </label>
                  <select
                    value={yearOfStudy}
                    onChange={(e) => setYearOfStudy(e.target.value)}
                    style={styles.select}
                  >
                    <option value={1}>1st Year (Freshman)</option>
                    <option value={2}>2nd Year (Sophomore)</option>
                    <option value={3}>3rd Year (Junior)</option>
                    <option value={4}>4th Year (Senior)</option>
                  </select>
                </div>

                <div style={styles.inputGroup}>
                  <label style={styles.label}>
                    <Award size={13} style={styles.fieldIcon} />
                    Current CGPA / GPA
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    value={cgpa}
                    onChange={(e) => setCgpa(e.target.value)}
                    style={styles.input}
                    placeholder="e.g. 8.50 or 3.80"
                  />
                </div>
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>
                  <Phone size={13} style={styles.fieldIcon} />
                  Phone Number
                </label>
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  style={styles.input}
                  placeholder="9876543210"
                />
              </div>

              <div style={styles.row}>
                <div style={styles.inputGroup}>
                  <label style={styles.label}>
                    <LinkedinIcon style={styles.fieldIcon} />
                    LinkedIn URL
                  </label>
                  <input
                    type="url"
                    value={linkedinUrl}
                    onChange={(e) => setLinkedinUrl(e.target.value)}
                    style={styles.input}
                    placeholder="https://linkedin.com/in/username"
                  />
                </div>

                <div style={styles.inputGroup}>
                  <label style={styles.label}>
                    <GithubIcon style={styles.fieldIcon} />
                    GitHub URL
                  </label>
                  <input
                    type="url"
                    value={githubUrl}
                    onChange={(e) => setGithubUrl(e.target.value)}
                    style={styles.input}
                    placeholder="https://github.com/username"
                  />
                </div>
              </div>

              <button type="submit" disabled={saving} style={styles.submitBtn}>
                <Save size={16} style={{ marginRight: 8 }} />
                {saving ? "Saving Changes..." : "Save Profile Details"}
              </button>
            </form>
          )}
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
    maxWidth: 800,
    margin: "0 auto",
    padding: "3rem 1.5rem"
  },
  card: {
    backgroundColor: "#ffffff",
    padding: "2.5rem",
    borderRadius: "1rem",
    boxShadow: "0 4px 6px -1px rgba(0,0,0,0.03), 0 2px 4px -1px rgba(0,0,0,0.02)",
    border: "1px solid rgba(229, 231, 235, 0.8)"
  },
  header: {
    textAlign: "center",
    marginBottom: "2.5rem"
  },
  title: {
    fontSize: "1.75rem",
    fontWeight: 800,
    color: "#111827",
    marginBottom: "0.5rem",
    letterSpacing: "-0.02em"
  },
  subtitle: {
    color: "#4b5563",
    fontSize: "0.95rem",
    lineHeight: 1.5
  },
  loaderContainer: {
    display: "flex",
    justifyContent: "center",
    padding: "3rem 0"
  },
  spinner: {
    width: 36,
    height: 36,
    border: "3px solid #e5e7eb",
    borderTopColor: "#4f46e5",
    borderRadius: "50%",
    animation: "spin 1s linear infinite"
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1.5rem"
  },
  row: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "1.5rem"
  },
  inputGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "0.5rem"
  },
  label: {
    display: "inline-flex",
    alignItems: "center",
    fontSize: "0.875rem",
    fontWeight: 600,
    color: "#374151"
  },
  fieldIcon: {
    marginRight: 6,
    color: "#9ca3af"
  },
  input: {
    padding: "0.625rem 0.875rem",
    fontSize: "0.95rem",
    border: "1px solid #d1d5db",
    borderRadius: "0.5rem",
    outline: "none",
    transition: "border-color 0.2s"
  },
  select: {
    padding: "0.625rem 0.875rem",
    fontSize: "0.95rem",
    border: "1px solid #d1d5db",
    borderRadius: "0.5rem",
    outline: "none",
    backgroundColor: "#ffffff",
    cursor: "pointer"
  },
  submitBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    border: "none",
    padding: "0.75rem",
    fontSize: "0.975rem",
    fontWeight: 600,
    borderRadius: "0.5rem",
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow: "0 4px 6px -1px rgba(79, 70, 229, 0.2)",
    transition: "background-color 0.2s",
    marginTop: "1rem"
  },
  errorAlert: {
    backgroundColor: "#fef2f2",
    border: "1px solid #fee2e2",
    color: "#b91c1c",
    padding: "0.75rem 1rem",
    borderRadius: "0.5rem",
    fontSize: "0.9rem",
    display: "flex",
    alignItems: "center",
    fontWeight: 500
  },
  successAlert: {
    backgroundColor: "#f0fdf4",
    border: "1px solid #dcfce7",
    color: "#15803d",
    padding: "0.75rem 1rem",
    borderRadius: "0.5rem",
    fontSize: "0.9rem",
    display: "flex",
    alignItems: "center",
    fontWeight: 500
  }
};

export default Profile;
