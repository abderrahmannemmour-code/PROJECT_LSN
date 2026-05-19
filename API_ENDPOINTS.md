# 📋 Stag.io — API Endpoints Reference

> **Base URL:** `/api/`
> **Authentication:** JWT (JSON Web Tokens) via `Authorization: Bearer <access_token>`

---

## Table of Contents

1. [Authentication & User Management](#1-authentication--user-management)
2. [Shared Notifications (All Roles)](#2-shared-notifications-all-roles)
3. [Student Endpoints](#3-student-endpoints)
4. [Company Endpoints](#4-company-endpoints)
5. [Administrator Endpoints](#5-administrator-endpoints)

---

## 1. Authentication & User Management

These endpoints handle registration, login, token management, and profile operations.

### 1.1 Registration

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:------------:|
| `POST` | `/api/user/register/student/` | Register a new student account | ❌ |
| `POST` | `/api/user/register/company/` | Register a new company account | ❌ |

### 1.2 Token (Login / Refresh)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:------------:|
| `POST` | `/api/user/token/` | Obtain JWT access + refresh token pair (login) | ❌ |
| `POST` | `/api/user/token/refresh/` | Refresh an expired access token using the refresh token | ❌ |

### 1.3 Account Management

| Method | Endpoint | Description | Auth Required | Permission |
|--------|----------|-------------|:------------:|------------|
| `GET` | `/api/user/me/` | Get the authenticated user's details | ✅ | Any authenticated user |
| `PATCH` | `/api/user/me/` | Update the authenticated user's basic info | ✅ | Any authenticated user |
| `GET` | `/api/user/me/student/` | Get student-specific profile details | ✅ | Student only |
| `PATCH` | `/api/user/me/student/` | Update student profile (full_name, wilaya, links) | ✅ | Student only |
| `GET` | `/api/user/me/company/` | Get company-specific profile details | ✅ | Company only |
| `PATCH` | `/api/user/me/company/` | Update company profile (name, description, wilaya, website) | ✅ | Company only |
| `PATCH` | `/api/user/me/upload-logo/` | Upload a logo image for the company | ✅ | Company only |
| `PATCH` | `/api/user/me/upload-profile-image/` | Upload a profile image for the student | ✅ | Student only |
| `DELETE` | `/api/user/<id>/delete/` | Delete any user by ID (superuser action) | ✅ | Admin (is_staff) |

### 1.4 API Documentation

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:------------:|
| `GET` | `/api/schema/` | Download the OpenAPI schema (YAML) | ❌ |
| `GET` | `/api/docs/` | Swagger UI interactive documentation | ❌ |

---

## 2. Shared Notifications (All Roles)

These endpoints are available to **any authenticated user** (student, company, or admin).

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:------------:|
| `GET` | `/api/notifications/` | List all notifications for the logged-in user | ✅ |
| `GET` | `/api/notifications/unread/` | List only unread notifications | ✅ |
| `PATCH` | `/api/notifications/<id>/read/` | Mark a single notification as read | ✅ |
| `PATCH` | `/api/notifications/read-all/` | Mark all notifications as read | ✅ |

---

## 3. Student Endpoints

> **Permission:** All endpoints require a logged-in user with `role = student`.

### 3.1 Skills Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/student/skills/` | List all available skills (used to populate skill selector) |
| `GET` | `/api/student/me/skills/` | List the student's selected skills |
| `POST` | `/api/student/me/skills/add/` | Add a skill to the student's profile. **Body:** `{ "skill_id": <int> }` |
| `DELETE` | `/api/student/me/skills/<id>/remove/` | Remove a skill from the student's profile |

### 3.2 Offer Search & Browse

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/student/offers/` | Browse & search all open internship offers (with filters — see below) |
| `GET` | `/api/student/offers/<id>/` | View full details of a specific offer (includes `already_applied` flag) |

**Available query parameters for `/api/student/offers/`:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search in title and description |
| `wilaya` | string | Filter by wilaya (e.g. `19 - Sétif`) |
| `skills` | string | Comma-separated skill IDs (e.g. `1,3,5`) — returns offers matching **all** |
| `type` | string | `paid` or `unpaid` |
| `duration` | string | `short` (14–28 days), `medium` (29–60 days), `long` (60+ days) |
| `ordering` | string | `recent` (default), `salary_high`, `start_soon` |

### 3.3 Applications

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/student/offers/<id>/apply/` | Apply to an internship offer (creates application with status `PENDING`) |
| `GET` | `/api/student/applications/` | List all of the student's applications (ordered by most recent) |
| `GET` | `/api/student/applications/<id>/` | View full details of a specific application |
| `GET` | `/api/student/applications/<id>/document/` | Download internship agreement PDF (only when status = `VALIDATED`) |

### 3.4 Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/student/documents/` | List all generated internship agreements (documents) for the student |

### 3.5 Digital CV

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/student/universities/` | List all universities (used for the university dropdown) |
| `GET` | `/api/student/me/cv/` | View the student's Digital CV |
| `PATCH` | `/api/student/me/cv/` | Update Digital CV fields (university, academic year, summary, github, portfolio) |

---

## 4. Company Endpoints

> **Permission:** All endpoints require a logged-in user with `role = company`.

### 4.1 Offer Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/company/offers/` | List all offers created by this company |
| `POST` | `/api/company/offers/` | Create a new internship offer |
| `GET` | `/api/company/offers/<id>/` | View a specific offer's details |
| `PATCH` | `/api/company/offers/<id>/` | Update an existing offer |
| `DELETE` | `/api/company/offers/<id>/` | Delete an offer |

### 4.2 Applicant Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/company/offers/<id>/applicants/` | List all students who applied to a specific offer |
| `GET` | `/api/company/applications/` | List all applicants across all of the company's offers |
| `POST` | `/api/company/applications/<id>/accept/` | Accept a student's application (notifies student + university admins) |
| `POST` | `/api/company/applications/<id>/reject/` | Reject a student's application (notifies the student) |

---

## 5. Administrator Endpoints

> **Permission:** All endpoints require a logged-in user with `role = admin` (university administrator).
> **Scope:** Data is scoped to the admin's university — admins only see internships for students belonging to their university.

### 5.1 Notifications (Admin-specific)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/administration/notifications/` | List all notifications for the admin |
| `GET` | `/api/administration/notifications/unread/` | List unread notifications only |
| `PATCH` | `/api/administration/notifications/<id>/read/` | Mark a single notification as read |

### 5.2 Internship Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/administration/internships/` | List all internships for the admin's university |
| `GET` | `/api/administration/internships/<id>/` | View detailed information about a specific internship |
| `GET` | `/api/administration/internships/<id>/agreement/` | Download the internship agreement PDF |
| `PATCH` | `/api/administration/internships/<id>/validate/` | Validate an internship (generates agreement PDF, notifies student & company) |
| `PATCH` | `/api/administration/internships/<id>/reject/` | Reject an internship (notifies the company) |

### 5.3 Statistics & Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/administration/statistics/` | Dashboard summary — student counts, placement rate, status breakdown |
| `GET` | `/api/administration/statistics/companies/` | Company-level internship outcomes (per-company status counts) |
| `GET` | `/api/administration/statistics/companies/<company_id>/` | Detailed analytics for a single company (placement share %) |
| `GET` | `/api/administration/statistics/wilayas/` | Geographic distribution by wilaya. **Query:** `?source=student` or `?source=company` |
| `GET` | `/api/administration/statistics/trends/` | Monthly/weekly internship trend data. **Query:** `?period=monthly` or `?period=weekly` |
| `GET` | `/api/administration/statistics/agreements/` | Agreement generation coverage (generated vs. missing) |
| `GET` | `/api/administration/statistics/statuses/` | Focused status breakdown (pending, accepted, validated, rejected) |
| `GET` | `/api/administration/statistics/students/` | Student participation metrics (with vs. without internships) |

---

## Internship Status Flow

```
PENDING  ──→  ACCEPTED_BY_COMPANY  ──→  VALIDATED
   │                  │
   │                  ▼
   └──────────→  REJECTED
```

| Status | Set By | Description |
|--------|--------|-------------|
| `PENDING` | System | Created when a student applies to an offer |
| `ACCEPTED_BY_COMPANY` | Company | Company accepts the student's application |
| `VALIDATED` | Admin | University admin validates and generates the agreement PDF |
| `REJECTED` | Company / Admin | Application rejected at any stage |

---

## Quick Summary — Endpoint Count

| Section | Count |
|---------|:-----:|
| Authentication & User Management | 13 |
| Shared Notifications | 4 |
| Student Endpoints | 12 |
| Company Endpoints | 6 |
| Administrator Endpoints | 14 |
| **Total** | **49** |
