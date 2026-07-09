import React from "react";
import Header from "../../components/Header";
import { motion } from "framer-motion";
import { Calendar, Building, CheckCircle2, Clock } from "lucide-react";

const Applications = () => {
  const mockApplications = [
    { id: 1, title: "Software Engineer Intern", company: "Google", date: "2026-07-01", status: "Under Review" },
    { id: 2, title: "Data Analyst Intern", company: "Amazon", date: "2026-06-25", status: "Applied" }
  ];

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
          <h2 style={styles.title}>Your Applications</h2>
          <p style={styles.subtitle}>Track the status of internships you've applied for.</p>
          
          <div style={styles.list}>
            {mockApplications.map((app, index) => (
              <motion.div 
                key={app.id} 
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1, duration: 0.3 }}
                whileHover={{ x: 4, borderColor: "#c7d2fe" }}
                style={styles.row}
              >
                <div>
                  <h4 style={styles.jobTitle}>{app.title}</h4>
                  <span style={styles.company}>
                    <Building size={12} style={{ marginRight: 5, color: "#6b7280" }} />
                    {app.company}
                  </span>
                </div>
                <div style={styles.right}>
                  <span style={styles.date}>
                    <Calendar size={11} style={{ marginRight: 4 }} />
                    Applied: {app.date}
                  </span>
                  <span style={{
                    ...styles.status,
                    ...(app.status === "Under Review" ? styles.statusReview : {})
                  }}>
                    {app.status === "Under Review" ? (
                      <Clock size={11} style={{ marginRight: 4 }} />
                    ) : (
                      <CheckCircle2 size={11} style={{ marginRight: 4 }} />
                    )}
                    {app.status}
                  </span>
                </div>
              </motion.div>
            ))}
          </div>
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
  title: {
    fontSize: "1.75rem",
    fontWeight: 800,
    color: "#111827",
    marginBottom: "0.5rem",
    marginTop: 0,
    letterSpacing: "-0.02em"
  },
  subtitle: {
    color: "#4b5563",
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
    borderRadius: "0.75rem",
    border: "1px solid #e5e7eb",
    backgroundColor: "#f9fafb",
    transition: "border-color 0.2s"
  },
  jobTitle: {
    fontSize: "1.05rem",
    fontWeight: 700,
    color: "#111827",
    margin: 0
  },
  company: {
    display: "inline-flex",
    alignItems: "center",
    fontSize: "0.875rem",
    color: "#4b5563",
    marginTop: "0.25rem"
  },
  right: {
    display: "flex",
    flexDirection: "column",
    alignItems: "end",
    gap: "0.5rem"
  },
  date: {
    display: "inline-flex",
    alignItems: "center",
    fontSize: "0.8rem",
    color: "#9ca3af"
  },
  status: {
    display: "inline-flex",
    alignItems: "center",
    backgroundColor: "#e0e7ff",
    color: "#4f46e5",
    padding: "0.25rem 0.65rem",
    borderRadius: "9999px",
    fontSize: "0.75rem",
    fontWeight: 700,
    border: "1px solid #c7d2fe"
  },
  statusReview: {
    backgroundColor: "#fef3c7",
    color: "#d97706",
    border: "1px solid #fde68a"
  }
};

export default Applications;
