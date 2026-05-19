# 🚀 Stag.io — Internship Management Platform

Stag.io is a modern, comprehensive internship management platform designed to streamline the internship lifecycle. It bridges the gap between students looking for professional experience, companies searching for talent, and university administration overseeing academic requirements.

Built for the **L3TI Workshop 2025-2026**.

---

## 🌟 Key Features

Stag.io provides a dedicated workspace for each of the three main roles:

### 🎓 1. Student Dashboard
- **Digital CV & Profile**: Build a professional profile with links to GitHub, portfolio, and wilaya info.
- **Internship Workflow**: Apply for internships, follow your application progress in real-time, and manage validation.
- **Notifications Hub**: Get instantly notified when a company or administrator updates your status.

### 🏢 2. Company Portal
- **Talent Recruitment**: Review student applications, inspect digital CVs, and easily accept or reject candidates.
- **Company Branding**: Customize your public profile page with logos, links, and detailed company descriptions.
- **Notifications**: Stay informed on new applications and administrative milestones.

### 🏛️ 3. University Administration
- **Academic Supervision**: Validate, reject, track, and monitor all internships across the department.
- **Analytics & Statistics**: Gain high-level insights on internship rates, popular fields, and company partnerships.
- **System Settings**: View administrative logs and broadcast announcements/notifications.

---

## 📂 Repository Structure

This repository is unified as a monorepo containing both the business logic/API server and the rich client application interface:

```text
PROJECT_LSN/
├── Back-end/                # Django REST Framework API (Business & Data Layer)
│   ├── Docker-compose.yaml  # Docker environment for DB & API services
│   ├── Dockerfile           # Python/Django environment container recipe
│   ├── requirements.txt     # Python production packages
│   └── stag_io/             # Django project root
│       ├── administration/  # Admin views, notifications & logs logic
│       ├── company/         # Company profile & hiring logic
│       ├── core/            # Custom User model & DB health utilities
│       ├── student/         # Student CV & profile management logic
│       └── user/            # JWT Auth & account registration flow
│
└── Front-end/               # React + Vite Client Application (Presentation Layer)
    ├── package.json         # Front-end packages & scripts
    ├── vite.config.js       # Vite configuration
    ├── tailwind.config.js   # Styling configuration (Tailwind CSS v4)
    ├── index.html           # Main SPA entry point
    └── src/
        ├── api/             # Axios base configuration & API clients
        ├── components/      # Shared UI components (Layout, Cards, Modals)
        ├── context/         # AuthContext & global app state
        ├── pages/           # Pages by actor and auth state
        │   ├── admin/       # AdminDashboard, AdminNotifications
        │   ├── company/     # CompanyDashboard, CompanyProfile, CompanyNotifications
        │   ├── student/     # StudentDashboard, DigitalCV, ProfilePage, EditProfile
        │   └── *            # LandingPage, LoginPage, RegisterPage, Unauthorized
        └── main.jsx         # Application bootstrapping
```

---

## 💻 Tech Stack

### ⚙️ Back-end (API Layer)
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | Django 3.2 + DRF 3.12 | Robust web API backbone |
| **Authentication** | Simple JWT | Secure stateless token-based auth (30m access / 7d refresh) |
| **Database** | PostgreSQL 13 | Enterprise relational database |
| **API Docs** | drf-spectacular | Swagger / OpenAPI 3 interactive documentation |
| **Containerization** | Docker & Docker Compose | Uniform runtime environments |
| **Linting** | Flake8 | Clean Python code enforcement |

### 🎨 Front-end (Client Layer)
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Build & Tooling** | Vite 8.0 | Next-generation blazing fast build tool |
| **Library** | React 19.2 | Component-driven UI framework |
| **Routing** | React Router v7 | Seamless client-side routing & page guards |
| **Styling** | Tailwind CSS v4 + Styled Components | Utility-first custom design & responsive grids |
| **Visualization**| Recharts 3.8 | Clean analytical charts for dashboards |
| **Icons** | Lucide React | Modern, consistent stroke icons |
| **HTTP Client** | Axios | Configured client with interceptors for JWT injection |

---

## 🚀 Getting Started

### 🛠️ Prerequisites
- [Docker & Docker Compose](https://www.docker.com/products/docker-desktop/) (for Back-end)
- [Node.js v18+](https://nodejs.org/) & [npm](https://www.npmjs.com/) (for Front-end)

---

### 1. Running the Back-end (Dockerized)

The Back-end runs completely inside containerized environments for effortless setup:

```bash
# Navigate to the Back-end folder
cd Back-end

# Build and start the containers
docker-compose up --build
```

- 🌐 The server will start at **http://localhost:8000**.
- 🔄 Database migrations are applied automatically on startup.
- 📖 Swagger interactive UI is accessible at **http://localhost:8000/api/docs/**.

#### Useful Back-end Commands:
```bash
# Create a Django Admin / Superuser
docker-compose run --rm stag_io sh -c "python manage.py createsuperuser"

# Run the test suite
docker-compose run --rm stag_io sh -c "python manage.py test"

# Run Flake8 code linting
docker-compose run --rm stag_io sh -c "flake8"
```

---

### 2. Running the Front-end (Development Server)

The Front-end connects automatically to the backend API services:

```bash
# Navigate to the Front-end folder
cd Front-end

# Install local dependencies
npm install

# Run the development server
npm run dev
```

- 🌐 The development server starts at **http://localhost:5173** (or the next available port).
- ⚡ Changes to components will use Hot Module Replacement (HMR) for instant preview.

#### Useful Front-end Commands:
```bash
# Lint the Front-end files
npm run lint

# Build the optimized production bundle
npm run build

# Preview the built application locally
npm run preview
```

---

## 🔒 Security & User Roles

Stag.io implements role-based access control (RBAC). Upon login, the app inspects the payload and routes users to their respective sub-areas. Unauthorized access to pages is automatically intercepted and redirected to `/unauthorized`.

### Base Auth API Endpoints (Path: `/api/user/`)

| Method | Endpoint | Description | Auth Required |
| :---: | :--- | :--- | :---: |
| **POST** | `register/student/` | Register a new student account | None |
| **POST** | `register/company/` | Register a new company account | None |
| **POST** | `token/` | Obtain JWT access/refresh token pair | None |
| **POST** | `token/refresh/` | Refresh an expired access token | None |
| **GET** | `me/` | Get current logged-in user profile details | JWT |
| **PATCH**| `me/` | Update general user fields | JWT |
| **GET** | `me/student/` | Get digital CV information (Students) | JWT |
| **PATCH**| `me/student/` | Edit digital CV information (Students) | JWT |
| **GET** | `me/company/` | Get company business info (Companies) | JWT |
| **PATCH**| `me/company/` | Edit company business info (Companies) | JWT |
| **PATCH**| `me/upload-logo/` | Upload company brand logo (Companies) | JWT |
| **PATCH**| `me/upload-profile-image/`| Upload student avatar (Students) | JWT |
| **DELETE**| `<id>/delete/` | Delete a specific user profile | JWT (Admin Only) |

---

## 🤝 Contributing

1. Format and lint all Python files using `flake8` inside the docker container.
2. Ensure React components are modular and separated logically.
3. Keep environment secrets separate from codebase repository files.
