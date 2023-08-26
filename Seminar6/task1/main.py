from typing import List
import databases as databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, SecretStr

app = FastAPI()

DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(50))
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


class UserIn(BaseModel):
    username: str = Field(min_length=2, max_length=32)
    email: EmailStr
    password: SecretStr


class User(UserIn):
    id: int


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def get_all_users():
    return "hello world"


@app.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(count):
        query = users.insert().values(username=f'user{i}', email=f'mail{i}@mail.ru', password='123456')
        await database.execute(query)
    return {'message': f'{count} fake users created'}


@app.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}', response_model=User)
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post('/users/add/', response_model=User)
async def add_user(user: UserIn):
    query = users.insert().values(username=user.username, email=user.email, password=user.password.get_secret_value())
    last_record_id = await database.execute(query)
    return {**user.dict(), 'id': last_record_id}


@app.put('/users/update/{user_id}', response_model=UserIn)
async def update_user(user: UserIn, user_id: int):
    query = users.update().where(users.c.id == user_id).values(username=user.username, email=user.email,
                                                               password=user.password.get_secret_value())
    await database.execute(query)
    return {**user.dict(), "id": user_id}


@app.delete('/users/delete/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"status": f"user with id {user_id} is deleted"}
