from pydantic import BaseModel

class TodoCreate(BaseModel):
    task: str
    completed: bool = False

class TodoUpdate(BaseModel):
    task: str
    completed: bool

class TodoOut(TodoCreate):
    id: int
