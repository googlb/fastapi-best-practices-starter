from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.api.v1.router import api_v1_router


app = FastAPI(
    title="FastAPI Best Practices Starter",
    description="A production-grade FastAPI project template.",
    version="0.1.0",
)

# Add Scalar API documentation
@app.get("/scalar", response_class=HTMLResponse)
async def read_scalar():
    return """
        <!doctype html>
        <html>
        <head>
            <title>Scalar API Reference</title>
            <meta charset="utf-8" />
            <meta
            name="viewport"
            content="width=device-width, initial-scale=1" />
            <style>
            body {
                margin: 0;
            }
            </style>
        </head>
        <body>
            <script
            id="api-reference"
            data-url="/openapi.json"></script>
            <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
        </body>
        </html>
    """

@app.get("/")
async def root():
    return {"message": "Hello from fastapi-best-practices-starter!"}


# Include domain routers
app.include_router(api_v1_router, prefix=settings.API_V1_STR)