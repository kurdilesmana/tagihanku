from sqlalchemy import create_engine, MetaData
from databases import Database
from app.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_size=10,
    max_overflow=2,
    pool_recycle=300)
database = Database(settings.SQLALCHEMY_DATABASE_URI)
metadata = MetaData()
