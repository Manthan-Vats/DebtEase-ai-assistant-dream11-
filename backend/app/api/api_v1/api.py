from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, debts, expenses, incomes, chat, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(debts.router, prefix="/debts", tags=["debts"])
api_router.include_router(
    expenses.router, prefix="/expenses", tags=["expenses"])
api_router.include_router(incomes.router, prefix="/incomes", tags=["incomes"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(
    analytics.router, prefix="/analytics", tags=["analytics"])
