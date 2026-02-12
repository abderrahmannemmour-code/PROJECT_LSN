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

### Backend (Current Implementation)
*   **Framework:** Python Django 3.2 with Django REST Framework 3.12
*   **Database:** PostgreSQL 13 (Alpine)
*   **Containerization:** Docker & Docker Compose
*   **Linting:** Flake8

### Frontend (Planned)
*   To be implemented

## 📦 Installation & Setup

### Prerequisites
*   Docker & Docker Compose installed on your machine

### Backend Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/abderrahmannemmour-code/PROJECT_LSN.git
    cd PROJECT_LSN
    ```

2.  **Build and run with Docker Compose**
    ```bash
    cd Back-end
    docker-compose up --build
    ```
    This will:
    - Build the Django application image (Python 3.9 Alpine)
    - Start a PostgreSQL 13 database container
    - Start the Django development server on `http://localhost:8000`

3.  **Environment Variables** (configured in docker-compose.yaml)
    - `DB_HOST`: db
    - `DB_NAME`: devdb
    - `DB_USER`: devuser
    - `DB_PASS`: changeme

### Running Commands in the Container
```bash
# Run migrations
docker-compose run --rm stag_io sh -c "python manage.py migrate"

# Create superuser
docker-compose run --rm stag_io sh -c "python manage.py createsuperuser"

# Run tests
docker-compose run --rm stag_io sh -c "python manage.py test"

# Lint with flake8
docker-compose run --rm stag_io sh -c "flake8"
```

## 📁 Project Structure

```
Back-end/
├── Docker-compose.yaml     # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── requirements.txt        # Production dependencies
├── requirements.dev.txt    # Development dependencies (flake8)
└── stag_io/
    ├── manage.py           # Django management script
    ├── core/               # Core app with custom commands
    │   └── management/
    │       └── commands/
    │           └── wait_for_db.py  # Custom DB wait command
    └── stag_io/
        ├── settings.py     # Django settings
        ├── urls.py         # URL configuration
        └── wsgi.py         # WSGI entry point
```

## 📄 Project Context
*   **Course:** L3TI Workshop (Atelier)
*   **Semester:** 2nd Semester, 2025-2026
*   **Goal:** Strengthen University-Enterprise links and digitize administration.
