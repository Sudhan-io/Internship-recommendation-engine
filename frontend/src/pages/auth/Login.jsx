import React, { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import API from "../../services/api";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await API.post("/auth/login", { email, password });
      if (res.data.success) {
        login(res.data.data);
        navigate("/dashboard");
      } else {
        setError(res.data.message || "Invalid credentials");
      }
    } catch (err) {
      setError(
        err.response?.data?.message || 
        "Failed to connect to the backend server. Please verify it is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <div style={styles.header}>
          <h2 style={styles.title}>Sign in to InternMatch</h2>
          <p style={styles.subtitle}>Unlock personalized AI internship recommendations</p>
        </div>
        
        {error && <div style={styles.errorAlert}>{error}</div>}
        
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Email Address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={styles.input}
              placeholder="you@college.edu"
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
              placeholder="••••••••"
            />
          </div>
          
          <button type="submit" disabled={loading} style={styles.submitBtn}>
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
        
        <p style={styles.footer}>
          Don't have an account?{" "}
          <Link to="/register" style={styles.link}>
            Create one now
          </Link>
        </p>
      </div>
    </div>
  );
};

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#f3f4f6",
    fontFamily: "Inter, -apple-system, sans-serif"
  },
  card: {
    backgroundColor: "#ffffff",
    padding: "2.5rem",
    borderRadius: "0.75rem",
    boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    width: "100%",
    maxWidth: 420
  },
  header: {
    textAlign: "center",
    marginBottom: "2rem"
  },
  title: {
    fontSize: "1.75rem",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "0.5rem"
  },
  subtitle: {
    fontSize: "0.95rem",
    color: "#6b7280"
  },
  errorAlert: {
    backgroundColor: "#fef2f2",
    border: "1px solid #fee2e2",
    color: "#b91c1c",
    padding: "0.75rem 1rem",
    borderRadius: "0.375rem",
    fontSize: "0.9rem",
    marginBottom: "1.5rem"
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
  submitBtn: {
    backgroundColor: "#4f46e5",
    color: "#ffffff",
    border: "none",
    padding: "0.75rem",
    fontSize: "0.95rem",
    fontWeight: 600,
    borderRadius: "0.375rem",
    cursor: "pointer",
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
    fontWeight: 500
  }
};

export default Login;
