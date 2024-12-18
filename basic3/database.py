from databases import Database
from sqlalchemy import create_engine, MetaData

#5432포트를 postgresql이 디폴트로 사용하고 있음!
DATABASE_URL = "postgresql://cakesniffer:1234@postgres:5432/CEL_todos_db"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
