# Task Tracker — MySQL + FastAPI + Vanilla JS

A full-stack task/project tracker built with a classical backend stack: MySQL, FastAPI, SQLAlchemy, JWT auth, and a plain HTML/CSS/JS frontend (no framework — kept simple so every line is explainable).

## Stack
- **Database:** MySQL (via XAMPP)
- **Backend:** FastAPI + SQLAlchemy + PyMySQL + python-jose (JWT) + passlib (bcrypt)
- **Frontend:** Plain HTML/CSS/JavaScript (fetch API, no build step)

## Setup

### 1. Start MySQL via XAMPP
Open the XAMPP control panel and start the **MySQL** module (you don't need Apache since the frontend is served by FastAPI itself).

### 2. Create the database
Open phpMyAdmin (or the MySQL CLI) and run:
```sql
CREATE DATABASE task_tracker;
```
If your XAMPP MySQL user/password differs from the default (`root`, no password), edit `DATABASE_URL` in `backend/database.py`.

### 3. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Run the server
```bash
uvicorn main:app --reload
```
Tables are created automatically on first run (`Base.metadata.create_all`).

### 5. Open the app
Visit **http://127.0.0.1:8000** — this serves the frontend directly.
Interactive API docs are at **http://127.0.0.1:8000/docs**.

## Project structure
```
task_tracker/
├── backend/
│   ├── main.py         # FastAPI app + all 12 routes
│   ├── models.py        # SQLAlchemy models: User, Project, Task
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── crud.py           # DB query functions
│   ├── auth.py            # Password hashing + JWT
│   ├── database.py         # MySQL connection/session
│   └── requirements.txt
└── frontend/
    ├── index.html        # Login / Register
    ├── projects.html      # List + create projects
    ├── tasks.html           # Tasks for one project, with status/priority filters
    ├── dashboard.html        # Summary stats
    ├── app.js                 # All API calls + auth token handling
    └── style.css
```

## Database schema
- **users**: id, name, email (unique), hashed_password, created_at
- **projects**: id, name, description, user_id (FK → users), created_at
- **tasks**: id, title, description, status (todo/in-progress/done), priority (low/medium/high), due_date, project_id (FK → projects), created_at

## API endpoints (12)
| Method | Path | Purpose |
|---|---|---|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Login, get JWT |
| GET | `/projects` | List my projects |
| POST | `/projects` | Create project |
| PUT | `/projects/{id}` | Update project |
| DELETE | `/projects/{id}` | Delete project |
| GET | `/projects/{id}/tasks` | List tasks in a project |
| POST | `/projects/{id}/tasks` | Create task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/tasks/filter?status=&priority=` | Filter tasks |
| GET | `/dashboard` | Summary counts |

## Design notes
- **Auth:** JWT stored in the browser's `localStorage`; every protected endpoint uses a `get_current_user` dependency that decodes the token and loads the user from the DB.
- **Ownership scoping:** Every project/task query is filtered by the logged-in user's `id` (via the project's `user_id`, or a join through `Project` for tasks) — one user can never see or modify another user's data.
- **Cascade deletes:** Deleting a project deletes its tasks (`cascade="all, delete-orphan"`); deleting a user deletes their projects.
- **Passwords:** hashed with bcrypt via passlib, never stored or returned in plaintext.
