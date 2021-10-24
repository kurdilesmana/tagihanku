from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    app, payment
)

api_router = APIRouter()
api_router.include_router(app.router, prefix="/app", tags=["app"])
api_router.include_router(payment.router, prefix="/payment", tags=["payment"])
