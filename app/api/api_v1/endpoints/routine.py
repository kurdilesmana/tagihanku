import json
from datetime import datetime
from typing import Any, Optional
from fastapi import APIRouter, Body
from starlette import status

from app import crud, utils, schemas

router = APIRouter()


@router.get("/routine/list", response_model=schemas.RespRoutineList)
async def routine_list(
    period_unit: str = "", period_value: str = "",
    page: Optional[int] = 0, show: Optional[int] = 15, keyword: Optional[str] = ""
) -> Any:
    try:
        listRoutines = await crud.routine.get_list_data(
            period_unit=period_unit, period_value=period_value, page=page, show=show, keyword=keyword)
        if not listRoutines:
            listRoutines = {"data": []}
        # --

        listRoutines.update({
            "currentPage": page or 1,
            "currentshow": show or listRoutines.get("totalRow", 0),
            "totalRow": listRoutines.get("totalRow", 0),
            "totalPage": listRoutines.get("totalPage", 0)
        })

        response = {
            "response_code": "00",
            "response_msg": "OK",
            "response_data": listRoutines
        }
    except Exception as e:
        response = utils.setExcMessage(e)
    # --

    utils.logger.info(response)

    return response
# --


@router.post("/routine/create", response_model=schemas.RespRoutine, status_code=status.HTTP_201_CREATED)
async def routine_create(
    request: schemas.RoutineCreate
) -> Any:
    try:
        data = await crud.routine.create(obj_in=request)

        response = {
            "response_code": "00",
            "response_msg": "OK",
            "response_data": data
        }
    except Exception as e:
        response = utils.setExcMessage(e)
    # --

    utils.logger.info(response)

    return response
# --


@router.get("/routine/{id}", response_model=schemas.RespRoutine)
async def routine_detail(
    id: int
) -> Any:
    try:
        data = await crud.routine.get(id=id)
        if not data:
            raise Exception(f"04::{utils.RC_CODE['04']}")
        # --

        response = {
            "response_code": "00",
            "response_msg": "OK",
            "response_data": data
        }
    except Exception as e:
        response = utils.setExcMessage(e)
    # --

    utils.logger.info(response)

    return response
# --


@router.put("/routine/{id}/update", response_model=schemas.RespRoutine)
async def routine_update(
    id: int,
    request: schemas.RoutineUpdate
) -> Any:
    try:
        data = await crud.routine.get(id=id)
        if not data:
            raise Exception(f"04::{utils.RC_CODE['04']}")
        # --

        request.updated_at = datetime.now()
        update = await crud.routine.update(db_obj=data, obj_in=request)

        response = {
            "response_code": "00",
            "response_msg": "OK",
            "response_data": update
        }
    except Exception as e:
        response = utils.setExcMessage(e)
    # --

    utils.logger.info(response)

    return response
# --


@router.delete("/routine/{id}/delete", response_model=schemas.BaseResponse)
async def routine_delete(
    id: int
) -> Any:
    try:
        data = await crud.routine.get(id=id)
        if not data:
            raise Exception(f"04::{utils.RC_CODE['04']}")
        # --

        delete = await crud.routine.delete(id=data.id)

        response = {
            "response_code": "00",
            "response_msg": "OK",
            "response_data": delete
        }
    except Exception as e:
        response = utils.setExcMessage(e)
    # --

    utils.logger.info(response)

    return response
# --
