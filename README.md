# FastAPI Best Practices Starter

This project is a production-grade starter template for building FastAPI applications, designed with Domain-Driven Design (DDD) and Vertical Slice Architecture principles. It emphasizes a clean, scalable, and maintainable codebase.

## Core Principles

-   **Domain-Driven Design (DDD)**: Code is organized around business domains (`app/domains`). Each domain is a self-contained vertical slice with its own routes, models, and business logic.
-   **Clean API Layer**: `main.py` is minimal. All API routes are aggregated in `app/api/v1/router.py`.
-   **Circular Dependency Prevention**: The project uses a central model registry at `app/db/base.py`. This allows Alembic to discover all database models for migrations without creating import cycles. Business logic **must not** import models from `app/db/base.py`.

## Project Architecture

```
fastapi-best-practices-starter/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Entrypoint: Initializes app, mounts the main API router
│   ├── api/                     # API Aggregation Layer
│   │   └── v1/
│   │       └── router.py        # Aggregates all domain routers, adds `/api/v1` prefix
│   ├── core/                    # Core Configuration (Settings, Security, Exceptions)
│   ├── db/                      # Database Infrastructure
│   │   └── base.py              # Model Registry: Imports all SQLModels for Alembic
│   ├── dependencies/            # Global Dependency Injection (e.g., DB Session)
│   ├── domains/                 # Business Domains (Vertical Slices)
│   │   ├── news/                # Example Domain
│   │   │   ├── router.py        # Domain-specific routes
│   │   │   ├── models.py        # SQLModel definitions
│   │   │   ├── schemas.py       # Pydantic DTOs for I/O
│   │   │   └── crud.py          # Database operations
│   │   └── user/                # User-related domain
│   └── utils/                   # Utility functions
├── alembic/
│   └── env.py                   # Configured to use app.db.base for metadata
├── .env
├── docker-compose.yml
└── pyproject.toml
```

## The `db/base.py` Pattern

This pattern is crucial for preventing circular dependencies while ensuring Alembic works correctly.

1.  **Model Definition**: All `SQLModel` classes are defined in their respective domain, e.g., `app/domains/news/models.py`.
2.  **Model Registration**: To make models discoverable by Alembic, they **must** be imported in `app/db/base.py`.
    ```python
    # app/db/base.py
    from sqlmodel import SQLModel
    from app.domains.news.models import News
    from app.domains.user.models import User # etc.
    ```
3.  **Usage Rule**: Business logic (e.g., in `crud.py` or `router.py`) **must** import models directly from their source, not from `app/db/base.py`.
    ```python
    # CORRECT: in app/domains/news/crud.py
    from app.domains.news.models import News

    # WRONG - DO NOT DO THIS:
    # from app.db.base import News
    ```

## Getting Started

### 1. Prerequisites

-   Docker
-   Python 3.9+
-   `uv` or `pip`

### 2. Setup

1.  **Clone the repository:** `git clone <your-repo-url>`
2.  **Configure Environment**: Create a `.env` file and fill in your database credentials and a secret key.
3.  **Install Dependencies**: `uv pip install -e .` or `pip install -e .`
4.  **Launch Services**: `docker-compose up --build`

### 3. Database Migrations

With the services running, execute these commands in a separate terminal:

1.  **Generate Migration** (after changing models):
    ```bash
    alembic revision --autogenerate -m "Describe your changes"
    ```
2.  **Apply Migration**:
    ```bash
    alembic upgrade head
    ```

### 4. Accessing the API

-   **API Base URL**: `http://localhost:8000/api/v1`
-   **Scalar UI**: `http://localhost:8000/scalar`
-   **Swagger UI**: `http://localhost:8000/docs`

## Adding a New Domain

1.  Create a new directory `app/domains/my_new_domain/`.
2.  Add your `models.py`, `router.py`, `schemas.py`, etc.
3.  In `app/db/base.py`, add `from app.domains.my_new_domain.models import MyModel`.
4.  In `app/api/v1/router.py`, import and include the new router.
5.  Generate a new migration (`alembic revision --autogenerate`) and apply it.
