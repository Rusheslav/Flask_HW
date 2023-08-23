from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

TASKS = []


class Task(BaseModel):
    id_: int
    title: str
    description: str
    status: str


@app.get('/tasks/')
async def all_tasts():
    return {'tasks': TASKS}


@app.post('/task/add')
async def add_task(task: Task):
    TASKS.append(task)
    return {'task': task, 'status': 'added'}


@app.put('/task/update/{task_id}')
async def update_task(task_id: int, task: Task):
    for t in TASKS:
        if t.id_ == task_id:
            t.name = task.title
            t.email = task.description
            t.status = task.status
            return {'task': t, 'status': 'added'}
        return HTTPException(404, 'Task not found')


@app.delete('/task/delete/{task_id}')
async def delete_task(task_id: int):
    for t in TASKS:
        if t.id_ == task_id:
            TASKS.remove(t)
            return {'status': 'deleted'}
    return HTTPException(404, 'Task not found')
