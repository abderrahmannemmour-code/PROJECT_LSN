// src/api/axios.js
// This is the MAIN HTTP client for all API calls.
//
// What it does:
// 1. Sets the base URL of your friend's backend (change this when he deploys)
// 2. Automatically adds the JWT token to EVERY request header
// 3. If a request fails because token expired → automatically refreshes token
//    and retries the request without you doing anything

import axios from "axios";

// ⚠️ Change this to your friend's backend URL when he deploys
// For now it points to localhost (both running on same PC)
const BASE_URL = "http://localhost:8000";

// Create the main axios instance
const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// REQUEST INTERCEPTOR
// Runs before EVERY API call
// Automatically adds: Authorization: Bearer <token>
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// RESPONSE INTERCEPTOR
// Runs after EVERY API response
// If we get a 401 (token expired) → get a new token and retry
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem("refresh_token");
        const res = await axios.post(`${BASE_URL}/api/user/token/refresh/`, {
          refresh: refreshToken,
        });
        const newToken = res.data.access;
        localStorage.setItem("access_token", newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch {
        // Refresh failed → logout user
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
