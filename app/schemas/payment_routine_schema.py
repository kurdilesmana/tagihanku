from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional, List


class PaymentRoutineBase(BaseModel):
    name: Optional[str]
    amount: Optional[int]
    period_unit: Optional[str]
    period_value: Optional[int]
    is_active: Optional[str]
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
    # --
# --


class PaymentRoutine(PaymentRoutineBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
    # --
# --


class PaymentRoutineCreate(PaymentRoutineBase):
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


class PaymentRoutineUpdate(PaymentRoutineBase):
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
