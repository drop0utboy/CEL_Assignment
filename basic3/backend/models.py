from sqlalchemy import Table, Column, Integer, String, Boolean
from database import metadata

todos = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task", String, nullable=False),
    Column("completed", Boolean, default=False),
)
