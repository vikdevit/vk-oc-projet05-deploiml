from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.routes import router
from app.api.auth import router as auth_router

app = FastAPI(
    title="API prediction départ salarié TechNova Partners ESN",
    version="1.0",
    description="ML API pour identifier si un salarié est susceptible de démissionner"
)

app.include_router(auth_router)
app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "API running"}


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "ML API is alive",
        "docs": "/docs"
    }


# ----------------------------
# SWAGGER JWT FIX (IMPORTANT)
# ----------------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # 🔐 SIMPLE BEARER AUTH (PAS OAUTH2)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # 🔐 appliquer uniquement aux endpoints protégés
    protected_paths = ["/predict", "/explain"]

    for path, methods in openapi_schema["paths"].items():
        if any(p in path for p in protected_paths):
            for method in methods:
                methods[method]["security"] = [
                    {"BearerAuth": []}
                ]

    app.openapi_schema = openapi_schema
    return openapi_schema


app.openapi = custom_openapi
