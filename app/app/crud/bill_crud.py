import math
from typing import Optional
from sqlalchemy import select, desc, asc, func, or_, and_
from sqlalchemy.sql.expression import join, table, text

from app.db import database
from app.crud.base import CRUDBase
from app.models.models import Bill
from app.schemas import BillCreate, BillUpdate


class CRUDBill(CRUDBase[Bill, BillCreate, BillUpdate]):
    async def get_list_data(
        self, *, page: Optional[int] = None, show: Optional[int] = None, keyword: Optional[str] = None
    ) -> Optional[Bill]:
        _tbl = self.table
        _col = _tbl.c
        _cond = text("1=1")

        db = await database.transaction()
        try:
            if keyword not in [None, ""]:
                _cond = _cond & (_col.name.like(f"{keyword}%") | _col.description.like(f"{keyword}%"))
            # --

            query = _tbl.select().where(_cond)
            if page and show:
                bills = await database.fetch_all(query=query)
                if not bills:
                    return None
                # --

                totalRows = len(bills)
                totalPage = totalRows/show

                query = query.offset((page-1)*show).limit(show)
                bills = await database.fetch_all(query=query)
            else:
                query = query.limit(20)
                bills = await database.fetch_all(query=query)
                if not bills:
                    return None
                # --

                totalRows = len(bills)
                totalPage = 1
            # --
        except Exception as e:
            await db.rollback()
            raise Exception(f"90::Rollback: Db transaction failed, {e}")
        else:
            await db.commit()
        # --

        return {
            "data": [{key: value for (key, value) in data.items()} for data in bills],
            "totalRow": totalRows,
            "totalPage": math.ceil(totalPage)
        }
    # --
# --


bill = CRUDBill(Bill)
