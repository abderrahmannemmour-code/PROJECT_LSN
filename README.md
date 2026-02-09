# Stag.io - Internship Management & Matching Platform

**Stag.io** is a full-stack web application designed to bridge the gap between Students, Companies, and University Administration. It streamlines the internship search process, facilitates student-company matching, and digitizes the administrative workflow for internship agreements (*Conventions de Stage*).

This project was developed as part of the **L3TI Workshop (Atelier) 2025-2026** to address the challenges of manual internship management.

## 🚀 Features

### 🎓 1. Student Space
*   **Secure Authentication:** Sign up/Login (Institutional Email integration recommended).
*   **Digital CV:** Build a profile with personal details, GitHub/Portfolio links, and specific skill tags (e.g., React, Java, Python).
*   **Smart Search:** Filter internship offers by location (Wilaya), technology, and type.
*   **Applications:** One-click application to interest companies.

### 🏢 2. Company Space (Recruiters)
*   **Brand Profile:** Manage company logo, description, and location.
*   **Offer Management:** Create, edit, and delete internship opportunities.
*   **Candidate Dashboard:** View applicants and change their status (**Accept** or **Refuse**).
    *   *Accepting a candidate triggers the administrative validation process.*

### 🏛️ 3. Administration Space
*   **Placement Validation:** Notifications when a company selects a student.
*   **Automated Documents:** Instantly generate official **Internship Agreements (PDF)** pre-filled with student, company, and university data.
*   **Statistics:** specific dashboards to track placed vs. unplaced students.

## 🛠️ Tech Stack

*   **Frontend:** ReactJS / VueJS / AngularJS (Choose one)
*   **Backend:** NodeJS (Express) / PHP (Laravel) / Python (Django/FastAPI)
*   **Database:** MongoDB / MySQL / PostgreSQL
*   **Authentication:** JWT (JSON Web Tokens)
*   **PDF Generation:** Libraries for dynamic PDF creation (e.g., PDFKit, FPDF, ReportLab)

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/stag-io.git
    cd stag-io
    ```

2.  **Backend Setup**
    ```bash
    cd backend
    # Install dependencies (Example for Node.js)
    npm install
    # Configure environment variables (.env)
    # Start the server
    npm start
    ```

3.  **Frontend Setup**
    ```bash
    cd frontend
    # Install dependencies
    npm install
    # Start the development server
    npm run dev
    ```

## 📄 Project Context
*   **Course:** L3TI Workshop (Atelier)
*   **Semester:** 2nd Semester, 2025-2026
*   **Goal:** Strengthen University-Enterprise links and digitize administration.
