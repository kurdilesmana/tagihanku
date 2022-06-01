from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional, List

from app.schemas.base_schema import Response, ResponseList


class BillBase(BaseModel):
    name: Optional[str]
    period_count: Optional[int]
    bill_amount: Optional[int]
    total_amount: Optional[int]
    detail_type: Optional[str]
    description: Optional[str]
    status: Optional[str] = "1"
    # created_at: Optional[datetime] = datetime.now()
    # updated_at: Optional[datetime] = datetime.now()
# --


class Bill(BillBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
    # --
# --


class BillCreate(BillBase):
    name: str
    period_count: int
    bill_amount: int
    total_amount: int
    detail_type: str
# --


class BillUpdate(BillBase):
    pass
# --


class BillDetailBase(BaseModel):
    bill_id: Optional[int]
    sequence_no: Optional[int]
    due_date: Optional[datetime]
    amount: Optional[int]
    pay_date: Optional[datetime]
    is_paid: Optional[str]
    receipt: Optional[str]
# --


class BillDetail(BillDetailBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
    # --
# --


class BillDetailCreate(BillDetailBase):
    bill_id: int
    sequence_no: int
    due_date: int
    amount: int
# --


class BillDetailUpdate(BillBase):
    pass
# --


# Request Schema
class ReqBillDetail(BaseModel):
    sequence_no: Optional[int]
    due_date: Optional[datetime]
    amount: Optional[int]
# --


class ReqBillCreate(BillCreate):
    bill_detail: Optional[ReqBillDetail]
# --


# Response Schema
class RespBill(Response):
    response_data: Optional[Bill]
# --


class BillList(ResponseList):
    data: List[Bill]
# --


class RespBillList(Response):
    response_data: Optional[BillList]
# --


# Example Request
class ExampleRequest(BaseModel):
    ReqBillCreateExp: dict = {
        "Automatic": {
            "summary": "Automatic",
            "description": "**Automatic** create bill detail.",
            "value": {
                "name": "Shopeepay",
                "period_count": 12,
                "bill_amount": 50000,
                "total_amount": 600000,
                "detail_type": "A",
                "description": "Bayar Kontrakkan Guys.",
                "bill_detail": []
            }
        },
        "Manual": {
            "summary": "Manual",
            "description": "A **manual** create bill detail.",
            "value": {
                "name": "Shopeepay",
                "period_count": 12,
                "bill_amount": 50000,
                "total_amount": 600000,
                "detail_type": "M",
                "description": "Bayar Kontrakkan Guys.",
                "bill_detail": [
                    {
                        "sequence_no": 1,
                        "due_date": "20/05/21",
                        "amount": 50000
                    },
                    {
                        "sequence_no": 2,
                        "due_date": "20/05/21",
                        "amount": 50000
                    }, {
                        "sequence_no": 3,
                        "due_date": "20/05/21",
                        "amount": 50000
                    }, {
                        "sequence_no": 4,
                        "due_date": "20/05/21",
                        "amount": 50000
                    },
                ]
            }
        }
    }
# --


ExpReqbill = ExampleRequest()
