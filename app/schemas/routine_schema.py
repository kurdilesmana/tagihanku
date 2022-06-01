from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional, List

from app.schemas.base_schema import Response, ResponseList


class RoutineBase(BaseModel):
    name: Optional[str]
    amount: Optional[int]
    period_unit: Optional[str]
    period_value: Optional[int]
    is_active: Optional[str]
    description: Optional[str]
# --


class Routine(RoutineBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
    # --
# --


class RoutineCreate(RoutineBase):
    name: str
    amount: int
    period_unit: str
    period_value: int
    is_active: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Kontrakkan",
                "amount": 500000,
                "period_unit": "M",
                "period_value": 10,
                "is_active": "T",
                "description": "Bayar Kontrakkan Guys."
            }
        }
    # --
# --


class RoutineUpdate(RoutineBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "name": "Kontrakkan",
                "amount": 500000,
                "period_unit": "M",
                "period_value": 10,
                "is_active": "T",
                "description": "Bayar Kontrakkan Guys."
            }
        }
    # --
# --


# Response Schema
class RespRoutine(Response):
    response_data: Optional[Routine]
# --


class RoutineList(ResponseList):
    data: List[Routine]
# --


class RespRoutineList(Response):
    response_data: Optional[RoutineList]
# --
