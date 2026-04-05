from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from app.core.config import settings
from app.db.database import engine, Base
from app.api.routers import auth, users, records
from app.core.exceptions import integrity_error_handler, generic_exception_handler

# Create database tables (assuming no Alembic migration for now)
# In a real-world scenario, you would use Alembic for migrations
Base.metadata.create_all(bind=engine)

description = """
Finance Data Processing API helps you manage and analyze personal or corporate financial records.

## Users
* **Create Users** (Admin only)
* **Read Users** (Admin only)

## Records
* **Create, Update, Delete** financial records (Admin only)
* **Read** financial records with filters (All logged-in users)

## Summaries
* **Read Dashboard Summaries** (Analyst and Admin)
"""

tags_metadata = [
    {
        "name": "Auth",
        "description": "Operations with Authentication. Provides JWT Bearer tokens.",
    },
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Records",
        "description": "Manage financial records and retrieve analytical dashboards.",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    contact={
        "name": "Backend Team",
        "email": "backend@zorvyn.com",
    }
)

# Register global exception handlers
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Connect modular routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(records.router, prefix=f"{settings.API_V1_STR}/records", tags=["Records"])

@app.get("/")
def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME} API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}