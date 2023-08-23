from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, SecretStr

app = FastAPI()

USERS = []


class User(BaseModel):
    id_: int
    name: str
    email: EmailStr
    password: SecretStr


@app.get('/users/')
async def all_users():
    return {'users': USERS}


@app.get('/users/{user_name}')
async def get_genre(user_name: str):
    result = []
    for user in USERS:
        if user.name == user_name:
            result.append(user)
    if not result:
        raise HTTPException(404, 'Users not found')
    return {'users': result}


@app.post('/user/add')
async def add_user(user: User):
    USERS.append(user)
    return {'user': user, 'status': 'added'}


@app.put('/user/update/{user_id}')
async def update_user(user_id: int, user: User):
    for u in USERS:
        if u.id_ == user_id:
            u.name = user.name
            u.email = user.email
            u.password = user.password
            return {'user': u, 'status': 'added'}
        return HTTPException(404, 'User not found')


@app.delete('/user/delete/{user_id}')
async def delete_user(user_id: int):
    for u in USERS:
        if u.id_ == user_id:
            USERS.remove(u)
            return {'status': 'deleted'}
    return HTTPException(404, 'User not found')
