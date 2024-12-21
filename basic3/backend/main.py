from fastapi import FastAPI, HTTPException
from schemas import TodoCreate, TodoUpdate, TodoOut
import crud
from database import database, metadata, engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# 데이터베이스 초기화
metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/todos/", response_model=TodoOut)
async def create_todo(todo: TodoCreate):
    return await crud.create_todo(todo.dict())

@app.get("/todos/", response_model=list[TodoOut])
async def read_todos():
    return await crud.get_all_todos()

@app.get("/todos/{id}", response_model=TodoOut)
async def read_todo_by_id(id: int):
    todo = await crud.get_todo_by_id(id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{id}", response_model=TodoOut)
async def update_todo(id: int, todo: TodoUpdate):
    existing_todo = await crud.get_todo_by_id(id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return await crud.update_todo(id, todo.dict())

@app.delete("/todos/{id}")
async def delete_todo(id: int):
    existing_todo = await crud.get_todo_by_id(id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    await crud.delete_todo(id)
    return {"message": "Todo deleted"}
from fastapi import FastAPI, HTTPException
from schemas import TodoCreate, TodoUpdate, TodoOut
import crud
from database import database, metadata, engine

app = FastAPI()

# 데이터베이스 초기화
metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/todos/", response_model=TodoOut)
async def create_todo(todo: TodoCreate):
    return await crud.create_todo(todo.dict())

@app.get("/todos/", response_model=list[TodoOut])
async def read_todos():
    return await crud.get_all_todos()

@app.get("/todos/{id}", response_model=TodoOut)
async def read_todo_by_id(id: int):
    todo = await crud.get_todo_by_id(id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{id}", response_model=TodoOut)
async def update_todo(id: int, todo: TodoUpdate):
    existing_todo = await crud.get_todo_by_id(id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return await crud.update_todo(id, todo.dict())

@app.delete("/todos/{id}")
async def delete_todo(id: int):
    existing_todo = await crud.get_todo_by_id(id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    await crud.delete_todo(id)
    return {"message": "Todo deleted"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React에서 FastAPI로 요청 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)