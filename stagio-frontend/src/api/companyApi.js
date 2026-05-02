// src/api/companyApi.js
// All API functions for the COMPANY role.
// Import these in CompanyDashboard.jsx

import api from "./axios";

// ── OFFERS ────────────────────────────────────────────────────────────────────

// Create a new internship offer
// data = { title, wilaya, duration, description, skills: ["React", "Python"] }
export const createOffer = (data) =>
  api.post("/api/company/offers/", data);

// Get all MY company's offers
export const getMyOffers = () =>
  api.get("/api/company/offers/");

// Get single offer details
export const getOffer = (id) =>
  api.get(`/api/company/offers/${id}/`);

// Edit an offer
// data = { title, wilaya, duration, description, skills }
export const updateOffer = (id, data) =>
  api.patch(`/api/company/offers/${id}/`, data);

// Delete an offer
export const deleteOffer = (id) =>
  api.delete(`/api/company/offers/${id}/`);

// ── APPLICANTS ────────────────────────────────────────────────────────────────

// Get all students who applied to a specific offer
// offerId = the id of the offer
export const getApplicants = (offerId) =>
  api.get(`/api/company/offers/${offerId}/applicants/`);

// Accept a student's application
// appId = the id of the application
// This also triggers a notification to the admin
export const acceptApplication = (appId) =>
  api.post(`/api/company/applications/${appId}/accept/`);

// Reject a student's application
export const rejectApplication = (appId) =>
  api.post(`/api/company/applications/${appId}/reject/`);

// ── NOTIFICATIONS ─────────────────────────────────────────────────────────────

// Get my notifications
export const getNotifications = () =>
  api.get("/api/company/notifications/");

// Mark a notification as read
export const markNotifRead = (id) =>
  api.patch(`/api/company/notifications/${id}/read/`);
