import logging
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi

# Import rate limiter
from api.limiter.limiter import limiter

# Import routers
from api.routers.oauth import router as oauth_router

# Import middlewares
from api.middleware.headers import add_header_middleware

# Import API config
from config.config import API_TITLE, API_DESCRIPTION, API_VERSION, API_DOCS_ENABLED

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    swagger_ui_parameters={
        "docExpansion": "list",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "filter": True,
        "syntaxHighlight.theme": "monakai"
    }
)

app.state.limiter = limiter

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Add middlewares
add_header_middleware(app)

# Include router(s)
app.include_router(oauth_router)

@app.get("/", include_in_schema=False)
@limiter.limit("10/second")
async def root(request: Request):
    if API_DOCS_ENABLED:
        return {"message": "API is running. See /docs for documentation.", "version": API_VERSION, "docs": "/docs"}
    else:
        return {"message": "API is running", "version": API_VERSION}