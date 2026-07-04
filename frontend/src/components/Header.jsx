import React, { useContext } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Header = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (!user) return null;

  const navItems = [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Profile", path: "/profile" },
    { name: "Recommendations", path: "/recommendations" },
    { name: "Applications", path: "/applications" }
  ];

  return (
    <header style={styles.header}>
      <div style={styles.container}>
        <Link to="/dashboard" style={styles.logo}>
          <span style={styles.logoAccent}>Intern</span>Match
        </Link>
        <nav style={styles.nav}>
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.name}
                to={item.path}
                style={{
                  ...styles.navLink,
                  ...(isActive ? styles.navLinkActive : {})
                }}
              >
                {item.name}
              </Link>
            );
          })}
        </nav>
        <div style={styles.profile}>
          <span style={styles.userName}>{user.name}</span>
          <button onClick={handleLogout} style={styles.logoutBtn}>
            Logout
          </button>
        </div>
      </div>
    </header>
  );
};

const styles = {
  header: {
    backgroundColor: "#ffffff",
    borderBottom: "1px solid #e5e7eb",
    position: "sticky",
    top: 0,
    zIndex: 50,
    boxShadow: "0 1px 3px rgba(0,0,0,0.05)"
  },
  container: {
    maxWidth: 1200,
    margin: "0 auto",
    padding: "0 1.5rem",
    height: "4.5rem",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between"
  },
  logo: {
    fontSize: "1.5rem",
    fontWeight: "bold",
    color: "#1f2937",
    textDecoration: "none",
    letterSpacing: "-0.025em"
  },
  logoAccent: {
    color: "#4f46e5"
  },
  nav: {
    display: "flex",
    gap: "1.5rem"
  },
  navLink: {
    color: "#4b5563",
    textDecoration: "none",
    fontWeight: 500,
    fontSize: "0.95rem",
    padding: "0.5rem 0.75rem",
    borderRadius: "0.375rem",
    transition: "all 0.2s"
  },
  navLinkActive: {
    color: "#4f46e5",
    backgroundColor: "#eef2ff"
  },
  profile: {
    display: "flex",
    alignItems: "center",
    gap: "1rem"
  },
  userName: {
    color: "#374151",
    fontSize: "0.9rem",
    fontWeight: 500
  },
  logoutBtn: {
    backgroundColor: "#f3f4f6",
    color: "#374151",
    border: "none",
    padding: "0.5rem 1rem",
    borderRadius: "0.375rem",
    fontSize: "0.9rem",
    fontWeight: 500,
    cursor: "pointer",
    transition: "all 0.2s"
  }
};

export default Header;
