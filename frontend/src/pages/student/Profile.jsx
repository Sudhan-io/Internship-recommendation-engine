import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../../components/Header";
import API from "../../services/api";

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
        <div style={styles.card}>
          <div style={styles.header}>
            <h2 style={styles.title}>Student Profile Setup</h2>
            <p style={styles.subtitle}>Provide your academic details and social profiles to optimize recommendation matching.</p>
          </div>

          {loading ? (
            <div style={styles.loaderContainer}>
              <div style={styles.spinner}></div>
              <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
            </div>
          ) : (
            <form onSubmit={handleSubmit} style={styles.form}>
              {error && <div style={styles.errorAlert}>{error}</div>}
              {success && <div style={styles.successAlert}>{success}</div>}

              <div style={styles.row}>
                <div style={styles.inputGroup}>
                  <label style={styles.label}>College/University Name</label>
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
                  <label style={styles.label}>Department/Major</label>
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
                  <label style={styles.label}>Year of Study</label>
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
                  <label style={styles.label}>Current CGPA / GPA</label>
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
                <label style={styles.label}>Phone Number</label>
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
                  <label style={styles.label}>LinkedIn URL</label>
                  <input
                    type="url"
                    value={linkedinUrl}
                    onChange={(e) => setLinkedinUrl(e.target.value)}
                    style={styles.input}
                    placeholder="https://linkedin.com/in/username"
                  />
                </div>

                <div style={styles.inputGroup}>
                  <label style={styles.label}>GitHub URL</label>
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
                {saving ? "Saving Changes..." : "Save Profile Details"}
              </button>
            </form>
          )}
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
    maxWidth: 800,
    margin: "0 auto",
    padding: "2rem 1.5rem"
  },
  card: {
    backgroundColor: "#ffffff",
    padding: "2.5rem",
    borderRadius: "0.75rem",
    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
    border: "1px solid #e5e7eb"
  },
  header: {
    textAlign: "center",
    marginBottom: "2.5rem"
  },
  title: {
    fontSize: "1.75rem",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "0.5rem"
  },
  subtitle: {
    color: "#6b7280",
    fontSize: "0.95rem"
  },
  loaderContainer: {
    display: "flex",
    justifyContent: "center",
    padding: "2rem 0"
  },
  spinner: {
    width: 32,
    height: 32,
    border: "3px solid #4f46e5",
    borderTopColor: "transparent",
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
    fontSize: "0.875rem",
    fontWeight: 500,
    color: "#374151"
  },
  input: {
    padding: "0.625rem 0.875rem",
    fontSize: "0.95rem",
    border: "1px solid #d1d5db",
    borderRadius: "0.375rem",
    outline: "none",
    transition: "border-color 0.2s"
  },
  select: {
    padding: "0.625rem 0.875rem",
    fontSize: "0.95rem",
    border: "1px solid #d1d5db",
    borderRadius: "0.375rem",
    outline: "none",
    backgroundColor: "#ffffff"
  },
  submitBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    border: "none",
    padding: "0.75rem",
    fontSize: "1rem",
    fontWeight: 600,
    borderRadius: "0.375rem",
    cursor: "pointer",
    transition: "background-color 0.2s",
    marginTop: "1rem"
  },
  errorAlert: {
    backgroundColor: "#fef2f2",
    border: "1px solid #fee2e2",
    color: "#b91c1c",
    padding: "0.75rem 1rem",
    borderRadius: "0.375rem",
    fontSize: "0.9rem"
  },
  successAlert: {
    backgroundColor: "#f0fdf4",
    border: "1px solid #dcfce7",
    color: "#15803d",
    padding: "0.75rem 1rem",
    borderRadius: "0.375rem",
    fontSize: "0.9rem"
  }
};

export default Profile;
