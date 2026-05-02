// src/api/studentApi.js
// All API functions for the STUDENT role.
// Import these in StudentDashboard.jsx instead of writing api.get() everywhere.
// When your friend finishes the backend, these just work automatically.

import api from "./axios";

// ── SKILLS ───────────────────────────────────────────────────────────────────

// Get ALL available skills (the full list to pick from)
// Used in: Skills tab — "Available Skills" section
export const getAllSkills = () =>
  api.get("/api/student/skills/");

// Get MY skills (skills I already added to my profile)
// Used in: Skills tab, Profile card
export const getMySkills = () =>
  api.get("/api/student/me/skills/");

// Add a skill to my profile
// skillId = the id of the skill from getAllSkills()
export const addSkill = (skillId) =>
  api.post("/api/student/me/skills/", { skill_id: skillId });

// Remove a skill from my profile
// id = the id of MY skill entry (from getMySkills)
export const removeSkill = (id) =>
  api.delete(`/api/student/me/skills/${id}/`);

// ── OFFERS ────────────────────────────────────────────────────────────────────

// Get all published offers — supports filters
// filters = { search: "react", wilaya: "Alger", type: "short" }
export const getOffers = (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.search) params.append("search", filters.search);
  if (filters.wilaya) params.append("wilaya", filters.wilaya);
  if (filters.type)   params.append("type",   filters.type);
  return api.get(`/api/student/offers/?${params.toString()}`);
};

// Get single offer details
export const getOffer = (id) =>
  api.get(`/api/student/offers/${id}/`);

// Apply to an offer
// Sends my profile to the company
export const applyToOffer = (id) =>
  api.post(`/api/student/offers/${id}/apply/`);

// ── APPLICATIONS ──────────────────────────────────────────────────────────────

// Get all my applications and their statuses
// Used in: Applications tab
export const getMyApplications = () =>
  api.get("/api/student/applications/");

// Get single application detail
export const getApplication = (id) =>
  api.get(`/api/student/applications/${id}/`);

// Download the agreement PDF (only works if status = validated)
// Returns a blob (binary file) that we save as PDF
export const downloadAgreement = (id) =>
  api.get(`/api/student/applications/${id}/document/`, {
    responseType: "blob",
  });

// ── NOTIFICATIONS ─────────────────────────────────────────────────────────────

// Get my notifications
export const getNotifications = () =>
  api.get("/api/student/notifications/");

// Mark a notification as read
export const markNotifRead = (id) =>
  api.patch(`/api/student/notifications/${id}/read/`);
