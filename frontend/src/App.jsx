import { Routes, Route } from "react-router-dom";

import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";

import Dashboard from "./pages/student/Dashboard";
import Profile from "./pages/student/Profile";
import Recommendations from "./pages/student/Recommendations";
import Applications from "./pages/student/Applications";

import AdminDashboard from "./pages/admin/Dashboard";
import ManageInternships from "./pages/admin/ManageInternships";

function App() {
  return (
    <Routes>

      <Route path="/" element={<h1>AI Internship Recommendation Engine</h1>} />

      <Route path="/login" element={<Login />} />

      <Route path="/register" element={<Register />} />

      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/profile" element={<Profile />} />

      <Route
        path="/recommendations"
        element={<Recommendations />}
      />

      <Route
        path="/applications"
        element={<Applications />}
      />

      <Route
        path="/admin"
        element={<AdminDashboard />}
      />

      <Route
        path="/admin/internships"
        element={<ManageInternships />}
      />

    </Routes>
  );
}

export default App;