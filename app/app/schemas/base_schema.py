from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional, List


class Response(BaseModel):
    response_code: str
    response_msg: str
# --


class ResponseList(BaseModel):
    data: List[dict]
    currentPage: Optional[int]
    currentshow: Optional[int]
    totalRow: Optional[int]
    totalPage: Optional[int]
# --


class BaseResponse(Response):
    response_data: Optional[Any]
# --


class BaseResponseList(Response):
    response_data: Optional[ResponseList]
# --
