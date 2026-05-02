// src/App.jsx
// This is the ROUTER of your app.
// It connects URLs to pages:
//   /login          → LoginPage
//   /register/...   → RegisterPage
//   /student        → StudentDashboard
//   /company        → CompanyDashboard
//   /admin          → AdminDashboard
// ProtectedRoute blocks pages if user is not logged in.
// RoleRedirect sends the user to the right dashboard after login.

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import ProtectedRoute   from "./components/ProtectedRoute";
import LoginPage        from "./pages/LoginPage";
import RegisterPage     from "./pages/RegisterPage";
import StudentDashboard from "./pages/student/StudentDashboard";
import CompanyDashboard from "./pages/company/CompanyDashboard";
import AdminDashboard   from "./pages/admin/AdminDashboard";
import LandingPage      from "./pages/LandingPage";

// After login, this checks the user's role and sends them
// to the right dashboard automatically
function RoleRedirect() {
  const { user } = useAuth();
  if (user?.role === "student") return <Navigate to="/student" replace />;
  if (user?.role === "company") return <Navigate to="/company" replace />;
  if (user?.role === "admin")   return <Navigate to="/admin"   replace />;
  // If role is unknown, go to student by default (for testing)
  return <Navigate to="/student" replace />;
}

export default function App() {
  return (
    // AuthProvider gives every page access to login/logout/user info
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* PUBLIC pages — no login needed */}
          <Route path="/"               element={<LandingPage />} />
          <Route path="/login"          element={<LoginPage />} />
          <Route path="/register/:type" element={<RegisterPage />} />
          <Route path="/register"       element={<Navigate to="/register/student" replace />} />

          {/* After login → go to the right dashboard */}
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <RoleRedirect />
            </ProtectedRoute>
          }/>

          {/* PROTECTED pages — must be logged in */}
          <Route path="/student" element={
            <ProtectedRoute>
              <StudentDashboard />
            </ProtectedRoute>
          }/>

          <Route path="/company" element={
            <ProtectedRoute>
              <CompanyDashboard />
            </ProtectedRoute>
          }/>

          <Route path="/admin" element={
            <ProtectedRoute>
              <AdminDashboard />
            </ProtectedRoute>
          }/>

          {/* Anything else → go to landing page */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
