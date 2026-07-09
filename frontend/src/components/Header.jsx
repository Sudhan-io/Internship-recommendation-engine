import React, { useContext } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { LogOut, Compass } from "lucide-react";

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
          <Compass size={20} style={{ marginRight: 8, color: "#4f46e5" }} />
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
            <LogOut size={13} style={{ marginRight: 6 }} />
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
    borderBottom: "1px solid rgba(229, 231, 235, 0.8)",
    position: "sticky",
    top: 0,
    zIndex: 50,
    boxShadow: "0 1px 2px 0 rgba(0, 0, 0, 0.02)"
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
    display: "inline-flex",
    alignItems: "center",
    fontSize: "1.35rem",
    fontWeight: 800,
    color: "#111827",
    textDecoration: "none",
    letterSpacing: "-0.03em"
  },
  logoAccent: {
    color: "#4f46e5"
  },
  nav: {
    display: "flex",
    gap: "0.5rem"
  },
  navLink: {
    color: "#4b5563",
    textDecoration: "none",
    fontWeight: 600,
    fontSize: "0.9rem",
    padding: "0.5rem 0.875rem",
    borderRadius: "0.5rem",
    transition: "all 0.2s"
  },
  navLinkActive: {
    color: "#4f46e5",
    backgroundColor: "#eef2ff"
  },
  profile: {
    display: "flex",
    alignItems: "center",
    gap: "1.25rem"
  },
  userName: {
    color: "#374151",
    fontSize: "0.875rem",
    fontWeight: 600
  },
  logoutBtn: {
    backgroundColor: "#f9fafb",
    color: "#4b5563",
    border: "1px solid #e5e7eb",
    padding: "0.5rem 0.875rem",
    borderRadius: "0.5rem",
    fontSize: "0.875rem",
    fontWeight: 600,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    transition: "all 0.2s"
  }
};

export default Header;
