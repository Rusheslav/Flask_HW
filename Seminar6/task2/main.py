# Создать API для управления списком задач.
# Каждая задача должна содержать поля "название", "описание"
# и "статус" (выполнена/не выполнена).
# API должен позволять выполнять CRUD операции с задачами

from typing import List
import databases as databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

DATABASE_URL = "sqlite:///task2base.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(120)),
    sqlalchemy.Column("description", sqlalchemy.String(500)),
    sqlalchemy.Column("status", sqlalchemy.Boolean)
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


class TaskIn(BaseModel):
    title: str = Field(max_length=120)
    description: str = Field(max_length=500)
    status: bool


class Task(TaskIn):
    id: int


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def say_hello():
    return "hello world"


@app.get('/fake_tasks/{count}')
async def create_tasks(count: int):
    for i in range(count):
        query = tasks.insert().values(title=f'task{i}', description=f'description for task number {i}',
                                      status=i % 2)
        await database.execute(query)
    return {'message': f'{count} fake tasks created'}


@app.get('/tasks/', response_model=List[Task])
async def get_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get('/tasks/{task_id}', response_model=Task)
async def get_task(task_id):
    query = tasks.select().where(tasks.c.id == task_id)
    return await database.fetch_one(query)


@app.post('/add_task/', response_model=Task)
async def add_task(task: TaskIn):
    query = tasks.insert().values(title=task.title, description=task.description, status=task.status)
    last_record_id = await database.execute(query)
    return {**task.dict(), 'id': last_record_id}


@app.put('/update_task/{task_id}')
async def update_task(task: TaskIn, task_id: int):
    query = tasks.update().where(tasks.c.id == task_id).values(title=task.title, description=task.description,
                                                               status=task.status)
    await database.execute(query)
    return {**task.dict(), "id": task_id}


@app.delete('/tasks/delete/{task_id}')
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {"status": f"task with id {task_id} is deleted"}
