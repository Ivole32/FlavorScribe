from fastapi import Request
from fastapi.responses import Response

# API config
from config.config import API_VERSION

def add_header_middleware(app):
    @app.middleware("http")
    async def header_middleware(request: Request, call_next):
        response: Response = await call_next(request)

        response.headers["X-API-Version"] = API_VERSION
        response.headers["X-Content-Type-Options"] = "nosniff"

        if request.method == "OPTIONS":
            pass
        else:
            # Prevent caching for all API requests for now
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, proxy-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

        return response
    
    return app