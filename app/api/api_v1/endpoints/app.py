from email import message
import json
from typing import Any, Optional
from fastapi import APIRouter, Body

import telepot
import telepot.aio

from app import crud, utils, schemas
from app.db import database

router = APIRouter()
TOKEN = "5458637763:AAGKDJTRPARSHqx1kJ0uSp3wUSbgzTDN3oM"
bot = telepot.aio.Bot(TOKEN)


@router.get("/hello")
async def hello_world() -> Any:
    return "Hello World!"
# --


@router.post("/ireport/status", response_model=schemas.BaseResponse)
async def status(
    username: str = Body(...),
    userid: str = Body(...)
) -> Any:
    transaction = await database.transaction()
    try:
        userchat = await crud.userchat.get_by_username_id(username, userid)
        if not userchat:
            raise Exception("99::Username not found!")
        # --

        response = {
            "response_code": "00",
            "response_msg": "success",
            "response_data": userchat
        }
    except Exception as e:
        response = utils.setExcMessage(str(e))
        await transaction.rollback()
    else:
        await transaction.commit()
    # --

    utils.logger.info(response)

    return response
# --


@router.post("/ireport/register", response_model=schemas.BaseResponse)
async def register(
    username: str = Body(...),
    userid: str = Body(...),
    roleid: str = Body(...)
) -> Any:
    transaction = await database.transaction()
    try:
        oUserchat = await crud.userchat.get_by_username_or_id(username, userid)
        if not oUserchat:
            await crud.userchat.create(obj_in={
                'username': username, 'is_active': 'F',
                'userid': userid, 'roleid': roleid
            })
        else:
            await crud.userchat.update(db_obj=oUserchat, obj_in={'username': username, 'userid': userid, 'roleid': roleid})
        # --

        response = {
            "response_code": "00",
            "response_msg": f"Data Behasil Diproses."
        }
    except Exception as e:
        response = utils.setExcMessage(str(e))
        await transaction.rollback()
    else:
        await transaction.commit()
    # --

    utils.logger.info(response)

    return response
# --


@router.post("/ireport/notification", response_model=schemas.BaseResponse)
async def notification(
    method: str = Body(...),
    username: str = Body(...),
    message: Optional[str] = Body('Hello!')
) -> Any:
    transaction = await database.transaction()
    try:
        userchat = await crud.userchat.get_by_username(username)
        if not userchat:
            raise Exception("99::Username not found!")
        # --

        status = ''
        userchatlist = None
        if method.lower() == 'new':
            userchatlist = await crud.userchat.get_by_rolecode(role='QC')
            msg = f"[NEW] {message} telah ditambahkan. Terimakasih."
        elif method.lower() == 'check':
            userchatlist = await crud.userchat.get_by_rolecode(role='MK')
            status = "checking QC"
            msg = f"[NEW] {message} telah ditambahkan, pengajuan sudah dilakukan proses {status}. Terimakasih."
        elif method.lower() == 'approve':
            userchatlist = await crud.userchat.get_by_rolecode(role='KU')
            status = "approve Pimpinan"
            msg = f"[NEW] {message} telah ditambahkan, pengajuan sudah dilakukan proses {status}. Terimakasih."
        else:
            status = "akhir dibagian Keuangan."
        # --

        # send message
        if method.lower() != "new":
            msg = f"[UPDATE] {message} sudah dilakukan proses {status}. Terimakasih."
            await bot.sendMessage(userchat.chat_id, msg)
        # --

        utils.logger.info(userchatlist)
        if userchatlist:
            for chat in userchatlist:
                utils.logger.info(f"{chat.username} {chat.chat_id} {msg}")
                await bot.sendMessage(chat.chat_id, msg)
                # --
            # --
        # --

        response = {
            "response_code": "00",
            "response_msg": "OK"
        }
    except Exception as e:
        response = utils.setExcMessage(str(e))
        await transaction.rollback()
    else:
        await transaction.commit()
    # --

    utils.logger.info(response)

    return response
# --
