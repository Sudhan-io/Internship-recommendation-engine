import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../../services/api";
import { motion } from "framer-motion";
import { Compass, AlertCircle, CheckCircle2 } from "lucide-react";

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const res = await API.post("/auth/register", {
        fullName: name,
        email,
        password
      });
      if (res.data.success) {
        setSuccess("Account registered successfully! Redirecting to login...");
        setTimeout(() => navigate("/login"), 2000);
      } else {
        setError(res.data.message || "Registration failed");
      }
    } catch (err) {
      setError(err.response?.data?.message || "An error occurred during registration");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        style={styles.card}
      >
        <div style={styles.header}>
          <div style={styles.logoContainer}>
            <Compass size={32} style={{ color: "#4f46e5", marginBottom: 12 }} />
            <h2 style={styles.logoText}>InternMatch</h2>
          </div>
          <h3 style={styles.title}>Create your account</h3>
          <p style={styles.subtitle}>Start matching with top-tier internships</p>
        </div>
        
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
        
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Full Name</label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={styles.input}
              placeholder="Alex Johnson"
            />
          </div>
          
          <div style={styles.inputGroup}>
            <label style={styles.label}>Email Address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={styles.input}
              placeholder="alex@college.edu"
            />
          </div>
          
          <div style={styles.inputGroup}>
            <label style={styles.label}>Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
              placeholder="Min. 8 characters"
              minLength={8}
            />
          </div>
          
          <button type="submit" disabled={loading} style={styles.submitBtn}>
            {loading ? "Registering..." : "Create Account"}
          </button>
        </form>
        
        <p style={styles.footer}>
          Already have an account?{" "}
          <Link to="/login" style={styles.link}>
            Sign in
          </Link>
        </p>
      </motion.div>
    </div>
  );
};

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%)",
    fontFamily: "Inter, -apple-system, sans-serif",
    padding: "1.5rem"
  },
  card: {
    backgroundColor: "#ffffff",
    padding: "3rem 2.5rem",
    borderRadius: "1rem",
    boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05)",
    border: "1px solid rgba(229, 231, 235, 0.8)",
    width: "100%",
    maxWidth: 420
  },
  header: {
    textAlign: "center",
    marginBottom: "2rem",
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  logoContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    marginBottom: "0.5rem"
  },
  logoText: {
    fontSize: "1.5rem",
    fontWeight: 800,
    color: "#111827",
    margin: 0,
    letterSpacing: "-0.03em"
  },
  title: {
    fontSize: "1.15rem",
    fontWeight: 700,
    color: "#374151",
    marginTop: "0.5rem",
    marginBottom: "0.25rem"
  },
  subtitle: {
    fontSize: "0.9rem",
    color: "#6b7280",
    lineHeight: 1.4,
    margin: 0
  },
  errorAlert: {
    backgroundColor: "#fef2f2",
    border: "1px solid #fee2e2",
    color: "#b91c1c",
    padding: "0.75rem 1rem",
    borderRadius: "0.5rem",
    fontSize: "0.9rem",
    marginBottom: "1.5rem",
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
    marginBottom: "1.5rem",
    display: "flex",
    alignItems: "center",
    fontWeight: 500
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1.25rem"
  },
  inputGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "0.5rem"
  },
  label: {
    fontSize: "0.85rem",
    fontWeight: 600,
    color: "#374151"
  },
  input: {
    padding: "0.625rem 0.875rem",
    fontSize: "0.95rem",
    border: "1px solid #d1d5db",
    borderRadius: "0.5rem",
    outline: "none",
    transition: "border-color 0.2s"
  },
  submitBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    border: "none",
    padding: "0.75rem",
    fontSize: "0.95rem",
    fontWeight: 600,
    borderRadius: "0.5rem",
    cursor: "pointer",
    boxShadow: "0 4px 6px -1px rgba(79, 70, 229, 0.2)",
    transition: "background-color 0.2s",
    marginTop: "0.5rem"
  },
  footer: {
    textAlign: "center",
    fontSize: "0.9rem",
    color: "#6b7280",
    marginTop: "1.5rem"
  },
  link: {
    color: "#4f46e5",
    textDecoration: "none",
    fontWeight: 600
  }
};

export default Register;
