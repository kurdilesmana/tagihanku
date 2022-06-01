import math
from typing import Optional
from sqlalchemy import select, desc, asc, func, or_, and_
from sqlalchemy.sql.expression import join, table, text

from app.db import database
from app.crud.base import CRUDBase
from app.models.models import PaymentRoutine, PaymentHistory
from app.schemas import PaymentRoutineCreate


class CRUDPaymentRoutine(CRUDBase[PaymentRoutine, PaymentRoutineCreate, PaymentRoutine]):
    async def get_list_data(
        self, *, period_unit: Optional[str] = None, period_value: Optional[int] = None,
        page: Optional[int] = None, show: Optional[int] = None, keyword: Optional[str] = None
    ) -> Optional[PaymentRoutine]:
        _tbl = self.table
        _col = _tbl.c
        _cond = text("1=1")

        db = await database.transaction()
        try:
            if keyword not in [None, ""]:
                _cond = _cond & (_col.name.like(f"{keyword}%") | _col.description.like(f"{keyword}%"))
            # --

            if period_unit not in [None, "", 0]:
                _cond = _cond & (_col.period_unit == period_unit)
            # --

            if period_value not in [None, "", 0]:
                _cond = _cond & (_col.period_value == period_value)
            # --

            query = _tbl.select().where(_cond)
            if page and show:
                routines = await database.fetch_all(query=query)
                if not routines:
                    return None
                # --

                totalRows = len(routines)
                totalPage = totalRows/show

                query = query.offset((page-1)*show).limit(show)
                routines = await database.fetch_all(query=query)
            else:
                query = query.limit(20)
                routines = await database.fetch_all(query=query)
                if not routines:
                    return None
                # --

                totalRows = len(routines)
                totalPage = 1
            # --
        except Exception as e:
            await db.rollback()
            raise Exception(f"90::Rollback: Db transaction failed, {e}")
        else:
            await db.commit()
        # --

        return {
            "data": [{key: value for (key, value) in data.items()} for data in routines],
            "totalRow": totalRows,
            "totalPage": math.ceil(totalPage)
        }
    # --
# --


paymentroutine = CRUDPaymentRoutine(PaymentRoutine)
