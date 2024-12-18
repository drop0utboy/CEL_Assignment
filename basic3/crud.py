from models import todos
from database import database

async def create_todo(todo: dict):
    query = todos.insert().values(**todo)
    todo_id = await database.execute(query)
    return {**todo, "id": todo_id}

async def get_all_todos():
    query = todos.select()
    return await database.fetch_all(query)

async def get_todo_by_id(todo_id: int):
    query = todos.select().where(todos.c.id == todo_id)
    return await database.fetch_one(query)

async def update_todo(todo_id: int, todo: dict):
    query = todos.update().where(todos.c.id == todo_id).values(**todo)
    await database.execute(query)
    return {**todo, "id": todo_id}

async def delete_todo(todo_id: int):
    query = todos.delete().where(todos.c.id == todo_id)
    await database.execute(query)
