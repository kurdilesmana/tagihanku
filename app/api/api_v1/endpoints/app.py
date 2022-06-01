import json
from typing import Any
from fastapi import APIRouter, Body
from sqlalchemy.log import echo_property

from app import crud, utils, schemas

router = APIRouter()


@router.get("/hello")
async def hello_world() -> Any:
    return "Hello World!"
# --
