from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.auth import auth_router
from routers.user_routers import user_router
from routers.currencies_routers import currency_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5173/dashboard",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)
app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
)
app.include_router(
    currency_router,
    prefix="/currencies",
    tags=["Currencies"]
)

