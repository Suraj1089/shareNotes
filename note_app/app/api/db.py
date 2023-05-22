import os 
from sqlalchemy import Column,String,create_engine,MetaData,Table,Integer
# from dotenv import load_dotenv
from datetime import datetime as dt 
from pytz import timezone as tz
from databases import Database

# load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URI")
# DATABASE_URL  = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("completed",String(8), default="False"),
    Column("created_date", String(50), default=dt.now(tz("US/Eastern")).strftime("%Y-%m-%d %H:%M"))
)
# Databases query builder

database = Database(DATABASE_URL)
