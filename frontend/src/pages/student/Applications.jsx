import React from "react";
import Header from "../../components/Header";

const Applications = () => {
  const mockApplications = [
    { id: 1, title: "Software Engineer Intern", company: "Google", date: "2026-07-01", status: "Under Review" },
    { id: 2, title: "Data Analyst Intern", company: "Amazon", date: "2026-06-25", status: "Applied" }
  ];

  return (
    <div style={styles.page}>
      <Header />
      <main style={styles.container}>
        <div style={styles.card}>
          <h2 style={styles.title}>Your Applications</h2>
          <p style={styles.subtitle}>Track the status of internships you've applied for.</p>
          
          <div style={styles.list}>
            {mockApplications.map(app => (
              <div key={app.id} style={styles.row}>
                <div>
                  <h4 style={styles.jobTitle}>{app.title}</h4>
                  <span style={styles.company}>{app.company}</span>
                </div>
                <div style={styles.right}>
                  <span style={styles.date}>Applied: {app.date}</span>
                  <span style={{
                    ...styles.status,
                    ...(app.status === "Under Review" ? styles.statusReview : {})
                  }}>{app.status}</span>
                </div>
              </div>
            ))}
          </div>
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
  title: {
    fontSize: "1.75rem",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "0.5rem",
    marginTop: 0
  },
  subtitle: {
    color: "#6b7280",
    fontSize: "0.95rem",
    marginBottom: "2rem"
  },
  list: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem"
  },
  row: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "1rem 1.25rem",
    borderRadius: "0.5rem",
    border: "1px solid #e5e7eb",
    backgroundColor: "#f9fafb"
  },
  jobTitle: {
    fontSize: "1.05rem",
    fontWeight: "bold",
    color: "#111827",
    margin: 0
  },
  company: {
    fontSize: "0.9rem",
    color: "#4b5563"
  },
  right: {
    display: "flex",
    flexDirection: "column",
    alignItems: "end",
    gap: "0.25rem"
  },
  date: {
    fontSize: "0.8rem",
    color: "#9ca3af"
  },
  status: {
    backgroundColor: "#eef2ff",
    color: "#4f46e5",
    padding: "0.125rem 0.5rem",
    borderRadius: "9999px",
    fontSize: "0.8rem",
    fontWeight: 600
  },
  statusReview: {
    backgroundColor: "#fef3c7",
    color: "#d97706"
  }
};

export default Applications;
