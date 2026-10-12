"""FastAPI application for Research Buddy."""

from __future__ import annotations

import logging
import os
import warnings

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ADK marks the skills toolset experimental and says so on every import.
warnings.filterwarnings("ignore", category=UserWarning, module=r"google\.adk")

from .routers import chat, skills  # noqa: E402

logging.getLogger("LiteLLM").setLevel(logging.WARNING)

app = FastAPI(title="Research Buddy API", version="1.0.0",
              docs_url="/api/docs", openapi_url="/api/openapi.json", redoc_url=None)

# The site and the API share an origin in production, so CORS is off unless asked for.
_origins = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "").split(",") if o.strip()]
if _origins:
    app.add_middleware(CORSMiddleware, allow_origins=_origins, allow_methods=["GET", "POST"],
                       allow_headers=["Content-Type", "X-LLM-Provider", "X-LLM-Model", "X-LLM-Key",
                                      "X-S2-Key", "X-NCBI-Key"])

app.include_router(skills.router, prefix="/api", tags=["catalog"])
app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    if request.url.path not in ("/api/skills", "/api/providers") and not request.url.path.startswith("/api/skills/"):
        response.headers.setdefault("Cache-Control", "no-store")
    return response


@app.exception_handler(HTTPException)
async def http_error(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"message": exc.detail}, status_code=exc.status_code, headers=exc.headers)


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    first = exc.errors()[0] if exc.errors() else {}
    where = ".".join(str(p) for p in first.get("loc", ()) if p != "body")
    message = str(first.get("msg", "Invalid request")).removeprefix("Value error, ")
    return JSONResponse({"message": f"{where}: {message}" if where else message}, status_code=422)
