import json
from datetime import datetime
from typing import Any, Optional
from fastapi import APIRouter, Body
from starlette import status

from app import crud, utils, schemas

router = APIRouter()


@router.get("/bill/list", response_model=schemas.RespBillList)
async def bill_list(
    page: Optional[int] = 0, show: Optional[int] = 15, keyword: Optional[str] = ""
) -> Any:
    try:
        listBills = await crud.bill.get_list_data(page=page, show=show, keyword=keyword)
        if not listBills:
            listBills = {"data": []}
        # --

        listBills.update({
            "currentPage": page or 1,
            "currentshow": show or listBills.get("totalRow", 0),
            "totalRow": listBills.get("totalRow", 0),
            "totalPage": listBills.get("totalPage", 0)
        })

        response = {
            "response_code": "00",
            "response_msg": "OK",
            "response_data": listBills
        }
    except Exception as e:
        response = utils.setExcMessage(e)
    # --

    utils.logger.info(response)

    return response
# --


@router.post("/bill/create", response_model=schemas.RespBill, status_code=status.HTTP_201_CREATED)
async def routine_create(
    request: schemas.ReqBillCreate = Body(..., examples=schemas.ExpReqbill.ReqBillCreateExp)
) -> Any:
    try:
        detailType = request.detail_type
        if detailType == "A":
            pass
        # --

        data = await crud.bill.create(obj_in=request)

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

'''
@router.get("/routine/{id}", response_model=schemas.RespPaymentRoutine)
async def routine_detail(
    id: int
) -> Any:
    try:
        data = await crud.paymentroutine.get(id=id)
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


@router.put("/routine/{id}/update", response_model=schemas.RespPaymentRoutine)
async def routine_update(
    id: int,
    request: schemas.PaymentRoutineUpdate
) -> Any:
    try:
        data = await crud.paymentroutine.get(id=id)
        if not data:
            raise Exception(f"04::{utils.RC_CODE['04']}")
        # --

        request.updated_at = datetime.now()
        update = await crud.paymentroutine.update(db_obj=data, obj_in=request)

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
        data = await crud.paymentroutine.get(id=id)
        if not data:
            raise Exception(f"04::{utils.RC_CODE['04']}")
        # --

        delete = await crud.paymentroutine.delete(id=data.id)

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
'''
