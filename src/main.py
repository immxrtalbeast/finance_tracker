import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.config import settings
from domain.errors.base_errors import Forbidden, NotFound
from domain.errors.user_errors import InvalidCredentials, UserAlreadyExists
from presentation.api import accounts, transactions, users

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(UserAlreadyExists)
async def user_exists_handler(request, exc):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(NotFound)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(InvalidCredentials)
async def invalid_password_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(Forbidden)
async def forbidden_handler(request, exc):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


@app.get("/health", tags=["Utils🛠️"])
async def projects_health():
    return {"message": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
