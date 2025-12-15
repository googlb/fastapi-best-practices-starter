# FastAPI Best Practices Starter

A production-grade starter template for building FastAPI applications with Domain-Driven Design (DDD) and modern architecture patterns. This project emphasizes clean, scalable, and maintainable codebase following industry best practices.

## Features

- **Domain-Driven Design (DDD)**: Organized around business domains with vertical slice architecture
- **Modern Tech Stack**: FastAPI, SQLModel, PostgreSQL, Alembic, Pydantic V2
- **Authentication & Authorization**: JWT-based auth system with role-based access control
- **API Documentation**: Scalar UI and Swagger UI for interactive API docs
- **Code Quality**: Integrated linting, formatting, and type checking
- **Database Management**: Automated migrations with Alembic
- **Development Tools**: Pre-configured scripts for common development tasks

## Tech Stack

- **Backend**: FastAPI with async support
- **ORM**: SQLModel (async)
- **Database**: PostgreSQL with asyncpg driver
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic V2
- **Database Migrations**: Alembic
- **Code Quality**: Ruff (linting & formatting), MyPy (type checking)
- **Testing**: Pytest with async support
- **Documentation**: Scalar UI and Swagger UI
- **Deployment**: Gunicorn for production

## Project Architecture

```
fastapi-best-practices-starter/
├── app/                        # Main application directory
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── api/                    # API aggregation layer
│   │   └── v1/
│   │       └── router.py        # Main API router
│   ├── core/                   # Core configurations
│   │   ├── config.py           # Application settings
│   │   ├── security.py         # Security utilities
│   │   ├── exceptions.py       # Custom exceptions
│   │   ├── logging.py          # Logging configuration
│   │   └── resp.py             # Response formatting
│   ├── db/                     # Database infrastructure
│   │   ├── base.py             # Model registry for Alembic
│   │   ├── crud_base.py        # Base CRUD operations
│   │   └── mixins.py           # Model mixins
│   ├── dependencies/           # Global dependencies
│   │   ├── auth.py             # Authentication dependencies
│   │   └── database.py         # Database session management
│   ├── system/                 # System domain (users, roles, etc.)
│   │   ├── api/                # API routes
│   │   │   ├── user.py         # User endpoints
│   │   │   ├── role.py         # Role endpoints
│   │   │   ├── menu.py         # Menu endpoints
│   │   │   ├── dict.py         # Dictionary endpoints
│   │   │   └── router.py       # Domain router aggregation
│   │   ├── crud/               # CRUD operations
│   │   │   ├── crud_user.py    # User CRUD
│   │   │   ├── crud_role.py    # Role CRUD
│   │   │   └── ...
│   │   ├── models.py           # SQLModel definitions
│   │   ├── schemas/            # Pydantic models
│   │   │   ├── user.py         # User schemas
│   │   │   ├── role.py         # Role schemas
│   │   │   └── ...
│   │   └── services/           # Business logic
│   │       └── user_service.py # User services
│   └── utils/                  # Utility functions
├── alembic/                    # Database migrations
│   ├── env.py                  # Alembic configuration
│   └── versions/               # Migration files
├── scripts/                    # Utility scripts
│   └── init_admin.py           # Admin initialization
├── tests/                      # Test files
├── .env.example                # Environment variables template
├── docker-compose.yml          # Docker configuration
├── pyproject.toml              # Project configuration
├── Makefile                    # Make commands
└── run.sh                      # Shell script for common tasks
```

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- `uv` package manager (recommended) or `pip`

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd fastapi-best-practices-starter
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secret key
   ```

3. **Install dependencies**:
   ```bash
   # Using uv (recommended)
   ./run.sh install
   # or
   make install
   # or directly
   uv sync --dev
   ```

4. **Set up the database**:
   ```bash
   # Generate and apply migrations
   ./run.sh migrate
   # or
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

5. **Initialize admin user**:
   ```bash
   ./run.sh init-admin
   # This creates an admin user with username: admin, password: abc123
   ```

### Running the Application

#### Development Mode

```bash
# Using the shell script (recommended)
./run.sh dev

# Using Makefile
make dev

# Direct command
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### Production Mode

```bash
# Using the shell script
./run.sh start

# Using Makefile
make start

# Direct command
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

Once the application is running, you can access:

- **Scalar UI**: `http://localhost:8001/scalar` (development) or `http://localhost:8000/scalar` (production)
- **Swagger UI**: `http://localhost:8001/docs` (development) or `http://localhost:8000/docs` (production)

## Authentication

The application uses JWT-based authentication. To access protected endpoints:

1. **Login** to get an access token:
   ```bash
   curl -X POST "http://localhost:8001/api/v1/sys/users/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "abc123"}'
   ```

2. **Use the token** in subsequent requests:
   ```bash
   curl -X GET "http://localhost:8001/api/v1/sys/users/me" \
        -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

## Development Workflow

### Code Quality

```bash
# Run linting
./run.sh lint
# or
make lint

# Format code
./run.sh format
# or
make format
```

### Testing

```bash
# Run tests
./run.sh test
# or
make test
# or directly
uv run pytest
```

### Database Migrations

```bash
# Generate a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

### Cleaning Up

```bash
# Clean cache files
./run.sh clean
# or
make clean
```

## CRUD Operations Standards

This project follows a strict naming convention for CRUD operations:

| Operation | Method Name | Return Type | Description |
|-----------|------------|-------------|-------------|
| Get by ID | `get` | `Optional[Model]` | Get a single record by primary key |
| Paginated List | `get_page` | `Tuple[List[Model], int]` | Get paginated results with total count |
| List | `get_list` | `List[Model]` | Get all records (for dropdowns, etc.) |
| Create | `create` | `Model` | Create a new record |
| Update | `update` | `Model` | Update an existing record |
| Delete | `delete` | `bool` | Delete a record |

## Adding a New Domain

1. **Create domain structure**:
   ```bash
   mkdir -p app/system/api
   mkdir -p app/system/crud
   mkdir -p app/system/schemas
   ```

2. **Create model** in `app/system/models.py`:
   ```python
   from sqlmodel import SQLModel, Field
   from app.db.mixins import BaseModel
   
   class NewModel(BaseModel, table=True):
       __tablename__ = "new_models"
       
       name: str = Field(index=True)
       description: Optional[str] = None
   ```

3. **Create schemas** in `app/system/schemas/new_model.py`:
   ```python
   from pydantic import BaseModel
   from typing import Optional
   
   class NewModelBase(BaseModel):
       name: str
       description: Optional[str] = None
   
   class NewModelCreate(NewModelBase):
       pass
   
   class NewModelUpdate(BaseModel):
       name: Optional[str] = None
       description: Optional[str] = None
   
   class NewModelResponse(NewModelBase):
       id: int
       
       class Config:
           from_attributes = True
   ```

4. **Create CRUD operations** in `app/system/crud/crud_new_model.py`:
   ```python
   from app.db.crud_base import CRUDBase
   from app.system.models import NewModel
   from app.system.schemas.new_model import NewModelCreate, NewModelUpdate
   
   class CRUDNewModel(CRUDBase[NewModel, NewModelCreate, NewModelUpdate]):
       pass
   
   crud_new_model = CRUDNewModel(NewModel)
   ```

5. **Create API endpoints** in `app/system/api/new_model.py`:
   ```python
   from fastapi import APIRouter, Depends, HTTPException
   from app.dependencies.database import get_session
   from app.system.crud.crud_new_model import crud_new_model
   from app.system.schemas.new_model import NewModelCreate, NewModelResponse
   
   router = APIRouter()
   
   @router.post("/", response_model=NewModelResponse)
   async def create_new_model(
       *,
       session: AsyncSession = Depends(get_session),
       new_model_in: NewModelCreate
   ):
       return await crud_new_model.create(session, obj_in=new_model_in)
   ```

6. **Register the router** in `app/system/api/router.py`:
   ```python
   from app.system.api import new_model
   
   api_router.include_router(new_model.router, prefix="/new-models", tags=["new-models"])
   ```

7. **Generate and apply migration**:
   ```bash
   alembic revision --autogenerate -m "Add new model"
   alembic upgrade head
   ```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=app

# JWT
SECRET_KEY=your_super_secret_key_change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Docker Support

The project includes Docker support with `docker-compose.yml`. To use Docker:

```bash
# Build and start services
docker-compose up --build

# Stop services
docker-compose down
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.
