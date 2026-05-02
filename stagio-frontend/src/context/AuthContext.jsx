// src/context/AuthContext.jsx
// This is a GLOBAL STATE for authentication.
// Think of it like a global variable that every page can read.
//
// It stores:
//   - user       → the logged in user's info (name, email, role)
//   - loading    → true while checking if user is logged in on app start
//   - isLoggedIn → true/false shortcut
//
// Every page can use: const { user, login, logout } = useAuth()

import { createContext, useContext, useState, useEffect } from "react";
import api from "../api/axios";

// Create the context (like creating a shared storage room)
const AuthContext = createContext(null);

// AuthProvider wraps the whole app in App.jsx
// Everything inside it can access auth data
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // When app first loads → check if there's a saved token
  // If yes → fetch user info and keep them logged in
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  // Fetch current user from GET /api/user/me/
  const fetchUser = async () => {
    try {
      const res = await api.get("/api/user/me/");
      setUser(res.data);
    } catch {
      // Token is invalid → clear it
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    } finally {
      setLoading(false);
    }
  };

  // LOGIN — called from LoginPage
  // Sends email + password to POST /api/user/token/
  // Saves both tokens and fetches user info
  const login = async (email, password) => {
    const res = await api.post("/api/user/token/", { email, password });
    localStorage.setItem("access_token", res.data.access);
    localStorage.setItem("refresh_token", res.data.refresh);
    await fetchUser();
    return res.data;
  };

  // LOGOUT — clears everything
  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    window.location.href = "/login";
  };

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      login,
      logout,
      isLoggedIn: !!user,
      // role helpers — adjust field name if your friend uses different names
      isStudent: user?.role === "student",
      isCompany: user?.role === "company",
      isAdmin: user?.role === "admin",
    }}>
      {children}
    </AuthContext.Provider>
  );
}

// useAuth() hook — call this in any component to get auth data
// Example: const { user, logout } = useAuth()
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
