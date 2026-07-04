"""
FastAPI application entrypoint for the AI Health Monitoring &
Early Virus Risk Detection Platform backend.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.database import init_db
from app.core.response import error_response

from app.api.v1 import auth, bp, symptoms, reports, dashboard, emergency

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for logging vitals/symptoms, computing early virus/health "
                 "risk scores, generating reports, and triggering emergency alerts.",
    version="1.0.0",
)

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Startup ----
@app.on_event("startup")
def on_startup():
    init_db()


# ---- Global exception handlers (keep response shape consistent) ----
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(str(exc.detail)),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response("Validation error", exc.errors()),
    )


# ---- Health check ----
@app.get("/", tags=["Health"])
def root():
    return {"success": True, "message": f"{settings.APP_NAME} is running", "data": None}


@app.get("/health", tags=["Health"])
def health_check():
    return {"success": True, "message": "OK", "data": {"status": "healthy"}}


# ---- Routers ----
API_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(bp.router, prefix=API_PREFIX)
app.include_router(symptoms.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)
app.include_router(dashboard.router, prefix=API_PREFIX)
app.include_router(emergency.router, prefix=API_PREFIX)
