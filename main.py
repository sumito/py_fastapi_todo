import json
from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine, Session, select
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import models.db as Db


#SQL MODEL
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
#FORM MODELS
class TodoCreate(BaseModel):
    content: str

class TodoUpdate(BaseModel):
    id: int
    content: str

class TodoDelete(BaseModel):
    id: int


# main
app = FastAPI()

# hello world
@app.get("/")
async def root():
    return {"message": "Hello World"}

# select list
@app.get("/todos/")
async def todo_list():
    with Session(Db.engine) as session:
        stmt = select(Todo)
        results = session.exec(stmt)
        todos = []
        for todo in results:
            todos.append(todo)


    return {"todos": todos}

# select one
@app.get("/todos/{_id}")
async def todo_find(_id:int):
    with Session(Db.engine) as session:
        stmt = select(Todo).where(Todo.id == _id)
        todo = session.exec(stmt).first()

    return {"todo": todo}


# create
@app.post("/todo")
async def todo_create(todo :TodoCreate):
    with Session(Db.engine) as session:        
        todo = Todo(content=todo.content)
        session.add(todo)
        session.commit()

    return True


# update
@app.patch("/todo")
async def todo_update(todoUpdate :TodoUpdate):
    with Session(Db.engine) as session:
        stmt = select(Todo).where(Todo.id == todoUpdate.id)
        todo = session.exec(stmt).first()
        todo.content = todoUpdate.content
        session.add(todo)
        session.commit()
        #更新したレコードの取得
        stmt = select(Todo).where(Todo.id == todoUpdate.id)
        todo = session.exec(stmt).first()

    return todo


# delete
@app.delete("/todo")
async def todo_delete(todoDelete :TodoDelete):
    with Session(Db.engine) as session:
        stmt = select(Todo).where(Todo.id == todoDelete.id)
        todo = session.exec(stmt).first()
        session.delete(todo)
        session.commit()

    return True

