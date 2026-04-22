from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.routes import router
from app.schemas import ErrorResponse
from app.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    await db.execute(
        """CREATE TABLE IF NOT EXISTS profiles (
            id BINARY(16) NOT NULL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            gender VARCHAR(50),
            gender_probability FLOAT,
            age INT,
            age_group VARCHAR(50),
            country_id VARCHAR(100),
            country_name VARCHAR(255),
            country_probability FLOAT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    app.state.db = db
    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

origins = settings.cors_origins
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
)

# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status="error",
            message=str(exc.detail),
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            status="error",
            message="Validation error",
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            status="error", 
            message="Internal server error").model_dump(),
    )
