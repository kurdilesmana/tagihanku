from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    app, bill, routine
)

api_router = APIRouter()
api_router.include_router(app.router, prefix="/app", tags=["app"])
api_router.include_router(bill.router, prefix="/payment", tags=["payment"])
api_router.include_router(routine.router, prefix="/payment", tags=["payment"])
