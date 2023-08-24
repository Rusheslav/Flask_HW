from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, SecretStr
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


class User(BaseModel):
    id_: int
    name: str
    email: EmailStr
    password: SecretStr


USERS = [
    User(id_=1, name="Alice", email="alice@example.com", password=SecretStr("alicepassword")),
    User(id_=2, name="Bob", email="bob@example.com", password=SecretStr("bobpassword")),
    User(id_=3, name="Charlie", email="charlie@example.com", password=SecretStr("charliepassword")),
]


@app.get('/users/', response_class=HTMLResponse)
async def all_users(request: Request):
    headers = ['id', 'Name', 'email']
    return templates.TemplateResponse('users.html', {'request': request, 'headers': headers, 'users': USERS})


@app.get('/users/{user_name}')
async def get_genre(user_name: str):
    result = []
    for user in USERS:
        if user.name == user_name:
            result.append(user)
    if not result:
        raise HTTPException(404, 'Users not found')
    return {'users': result}


@app.get('/user/add', response_class=HTMLResponse)
async def add_user_page(request: Request):
    return templates.TemplateResponse('add_user.html', {'request': request})


@app.post('/user/add')
async def add_user(name: str = Form(...), email: EmailStr = Form(...), password: SecretStr = Form(...)):
    user = User(id_=len(USERS) + 1, name=name, email=email, password=password)
    USERS.append(user)
    print(user)
    print(USERS)
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
