import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, Numeric, BigInteger, Text, column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base


class Bill(Base):
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    period_count = Column(Integer, nullable=False)
    bill_amount = Column(BigInteger, nullable=False)
    total_amount = Column(BigInteger, nullable=False)
    detail_type = Column(String(1))
    description = Column(String(255))
    status = Column(String(1))
    created_at = Column(DateTime, server_default=text("now()"))
    updated_at = Column(DateTime, server_default=text("now()"))

    bill = relationship("BillDetail")
# --


class BillDetail(Base):
    __tablename__ = 'bill_detail'

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey("bills.id", ondelete="CASCADE"))
    sequence_no = Column(Integer, nullable=False)
    due_date = Column(DateTime, nullable=False)
    amount = Column(BigInteger, nullable=False)
    pay_date = Column(DateTime)
    is_paid = Column(String(1), server_default=text("'F'"))
    receipt = Column(Text)
# --


class Routine(Base):
    __tablename__ = 'routines'

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    amount = Column(BigInteger, nullable=False)
    period_unit = Column(String(1), nullable=False)
    period_value = Column(Integer, nullable=False)
    is_active = Column(String(1), server_default=text("'F'"))
    description = Column(String(255))
    created_at = Column(DateTime, server_default=text("now()"))
    updated_at = Column(DateTime, server_default=text("now()"))

    Routine = relationship("RoutineHistory")
# --


class RoutineHistory(Base):
    __tablename__ = 'routine_history'

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey("routines.id", ondelete="CASCADE"))
    payment_date = Column(DateTime, nullable=False)
    amount = Column(BigInteger, nullable=False)
    receipt = Column(Text)
    description = Column(String(255))
# --


class UserChat(Base):
    __tablename__ = 'user_chat'

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    userid = Column(String(50), nullable=False)
    roleid = Column(String(10))
    chat_id = Column(String(20))
    is_active = Column(String(1), server_default=text("'F'"))
    created_at = Column(DateTime, server_default=text("'now()'"))
# --
