import math
from typing import List, Optional
from sqlalchemy import select, desc, asc, func, or_, and_
from sqlalchemy.sql.expression import join, table, text

from app.db import database
from app.crud.base import CRUDBase
from app.models.models import UserChat


class CRUDUserChat(CRUDBase[UserChat, UserChat, UserChat]):
    async def get_by_username(self, username: str) -> Optional[UserChat]:
        _tbl = self.table
        _col = _tbl.c
        _cond = (func.lower(_col.username) == username.lower())

        query = _tbl.select().where(_cond)
        data = await database.fetch_one(query=query)
        if not data:
            return None
        # --

        return UserChat(**data)
    # --

    async def get_by_userid(self, userid: str) -> Optional[UserChat]:
        _tbl = self.table
        _col = _tbl.c
        _cond = (func.lower(_col.userid) == userid.lower())

        query = _tbl.select().where(_cond)
        data = await database.fetch_one(query=query)
        if not data:
            return None
        # --

        return UserChat(**data)
    # --

    async def get_by_username_id(self, username: str, userid: str) -> Optional[UserChat]:
        _tbl = self.table
        _col = _tbl.c
        _cond = (
            (func.lower(_col.userid) == userid.lower()) &
            (func.lower(_col.username) == username.lower())
        )

        query = _tbl.select().where(_cond)
        data = await database.fetch_one(query=query)
        if not data:
            return None
        # --

        return UserChat(**data)
    # --

    async def get_by_username_or_id(self, username: str, userid: str) -> Optional[UserChat]:
        _tbl = self.table
        _col = _tbl.c
        _cond = (
            (func.lower(_col.userid) == userid.lower()) |
            (func.lower(_col.username) == username.lower())
        )

        query = _tbl.select().where(_cond)
        data = await database.fetch_one(query=query)
        if not data:
            return None
        # --

        return UserChat(**data)
    # --

    async def get_by_rolecode(self, role: str) -> Optional[List[UserChat]]:
        _tbl = self.table
        _col = _tbl.c
        _cond = (
            (_col.roleid == role) &
            (_col.is_active == "T")
        )

        query = _tbl.select().where(_cond)
        data = await database.fetch_all(query=query)
        if not data:
            return None
        # --

        return [UserChat(**chatid) for chatid in data]
    # --
# --


userchat = CRUDUserChat(UserChat)
