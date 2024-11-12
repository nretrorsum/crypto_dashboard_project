from fastapi import FastAPI
from auth.auth import auth_router
from routers.user_routers import user_router
from routers.currencies_routers import currency_router
app = FastAPI()
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

