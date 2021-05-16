from fastapi import APIRouter

from app.routers import external_apis, accounts, platforms

api_router = APIRouter()
api_router.include_router(external_apis.router)
api_router.include_router(accounts.router)
api_router.include_router(platforms.router)
