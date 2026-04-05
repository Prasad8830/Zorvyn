# Finance Data Processing and Access Control Backend

## 🎯 Objective
A Finance Data Processing and Access Control Backend built using FastAPI, PostgreSQL, SQLAlchemy ORM, Pydantic, and JWT authentication. This system serves as a backend for a finance dashboard where users interact with financial records based on role-based access control (RBAC).

---

## 🏗️ Architecture & Folder Structure

The application follows a clean, modular architecture separating concerns into distinct layers:

```text
finance_backend/
├── app/
│   ├── api/                 # API Routes and Dependencies
│   │   ├── dependencies.py  # JWT extraction, DB session, Role checking
│   │   └── routers/
│   │       ├── auth.py      # Authentication and Login endpoints
│   │       ├── users.py     # User management (Admin only)
│   │       └── records.py   # Financial records & summary APIs
│   ├── core/                # Core Configuration
│   │   ├── config.py        # Environment variables & constants
│   │   └── security.py      # Password hashing & JWT generation logic
│   ├── db/                  # Database Connections & ORM
│   │   ├── database.py      # Engine and session maker
│   │   └── models.py        # SQLAlchemy relational models
│   ├── schemas/             # Pydantic validation schemas
│   │   ├── user.py          # Request/response schemas for users
│   │   └── record.py        # Request/response schemas for records
│   ├── services/            # Business Logic layer
│   │   └── record_service.py# Aggregation logic and complex DB queries
│   └── main.py              # FastAPI application instance
├── requirements.txt         # Project dependencies
└── .env                     # Environment variables (DB URL, JWT Secret)
```

---

## 🗄️ Database Schema Design (PostgreSQL)

### Table: `users`
*   `id`: UUID (Primary Key)
*   `email`: String (Unique, Indexed)
*   `hashed_password`: String
*   `role`: Enum (`viewer`, `analyst`, `admin`)
*   `is_active`: Boolean (Default: True)
*   `created_at`: DateTime (Default: now)

### Table: `financial_records`
*   `id`: UUID (Primary Key)
*   `owner_id`: UUID (Foreign Key -> users.id)
*   `amount`: Numeric/Decimal
*   `transaction_type`: Enum (`income`, `expense`)
*   `category`: String (e.g., "Salary", "Software", "Travel")
*   `transaction_date`: Date
*   `notes`: Text (Nullable)
*   `created_at`: DateTime (Default: now)

---

## 🔐 Role-Based Access Control (RBAC) Matrix

Strict permission enforcement using FastAPI dependencies:

| Endpoint Resource | Viewer | Analyst | Admin |
| :--- | :---: | :---: | :---: |
| **Auth** (`/auth/login`) | ✅ | ✅ | ✅ |
| **Users** (`/users/` CRUD) | ❌ | ❌ | ✅ |
| **Records** (`GET /records/`) | ✅ | ✅ | ✅ |
| **Records** (`POST /records/`) | ❌ | ❌ | ✅ |
| **Records** (`PUT/DELETE /records/`) | ❌ | ❌ | ✅ |
| **Summaries** (`GET /records/summary`) | ❌ | ✅ | ✅ |

---

## 🔌 API Contract

### Authentication
*   `POST /api/auth/login` -> Returns JWT access token.

### User Management
*   `POST /api/users/` -> Create a new user (Admin only).
*   `GET /api/users/` -> List all users (Admin only).

### Financial Records
*   `POST /api/records/` -> Create a financial record (Admin only).
*   `GET /api/records/` -> List records with filters (`?type=income&category=Salary&start_date=YYYY-MM-DD`). (All roles).
*   `PUT /api/records/{id}` -> Update a record (Admin only).
*   `DELETE /api/records/{id}` -> Delete a record (Admin only).

### Dashboard Summaries
*   `GET /api/records/summary` -> Returns total income, total expenses, net balance. (Analyst, Admin).
*   `GET /api/records/summary/category` -> Returns category-wise totals. (Analyst, Admin).

## 🛠️ Technologies Used
- **FastAPI**: High-performance web framework for APIs.
- **PostgreSQL**: Relational database for persistent storage.
- **SQLAlchemy (ORM)**: Database interaction and query building.
- **Pydantic**: Data validation and serialization.
- **python-jose & passlib**: JWT authentication, validation, and bcrypt password hashing.
- **Docker**: For running the PostgreSQL database locally without polluting the host environment.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Docker (for PostgreSQL database)

### 2. Setup Database
Spin up a local PostgreSQL instance using Docker mapped to port `5434` (to avoid conflicts):
```bash
docker run --name zorvyn-finance-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=finance_db -p 5434:5432 -d postgres:15
```

### 3. Install Dependencies
Create a virtual environment and install the required Python packages:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Create the Initial Admin User
Because the API strictly enforces that only `admin` users can create new accounts, you need a way to log in for the very first time. We created an initial seed script to bootstrap this:
```bash
export PYTHONPATH=.
python seed_admin.py
```
This generates a system super-admin:
- **Email/Username**: `admin@zorvyn.com`
- **Password**: `adminpassword123`

### 5. Run the Server
Start the Uvicorn ASGI server:
```bash
uvicorn app.main:app --reload
```

---

## 🔑 How to Log In & Use Swagger

FastAPI auto-generates beautiful documentation where you can test the APIs natively.

1. Navigate to the interactive API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
2. Click the green **Authorize** button at the top right of the page.
3. In the OAuth2 login modal that appears, fill out:
   - **username**: Enter `admin@zorvyn.com` (In FastAPI, the username field maps to our email).
   - **password**: Enter `adminpassword123`
   - **client_id & client_secret**: *Leave these completely blank. They are only used for external provider integrations.*
4. Click **Authorize** and then click **Close**.
5. You now have an active JWT Bearer token! Any API requests you execute through the Swagger UI will automatically include this token in the `Authorization` header, granting you full Administrator permissions.
