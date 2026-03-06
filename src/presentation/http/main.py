from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.settings import settings
import logging
from .routes import (
    health_routes,
    user_routes,
    role_routes
)
from config.dependencies import (
    configure_di, 
    shutdown_di
)
from config.logging import setup_logging
from .errors import add_exception_handlers
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

setup_logging()
logger = logging.getLogger("app.presentation.http.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_di()
    logger.info("User Service starting up")
    try:
        yield
    finally:
        try:
            await shutdown_di()
        except Exception as e:
            logger.exception("Error during DI shutdown: %s", e)
        logger.info("User Service stopped")

app = FastAPI(title=settings.app_name, lifespan=lifespan)

add_exception_handlers(app)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)

app.include_router(health_routes.router)
app.include_router(user_routes.router)
app.include_router(role_routes.router)

logger.info("User Service Ok")