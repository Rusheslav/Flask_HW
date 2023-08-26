from typing import List
import databases as databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, SecretStr
from sqlalchemy import ForeignKey, Enum
import enum
from datetime import date, datetime

app = FastAPI()

DATABASE_URL = "sqlite:///eshop.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

customers = sqlalchemy.Table(
    "customers", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(50))
)

items = sqlalchemy.Table(
    "items", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(500)),
    sqlalchemy.Column("price", sqlalchemy.Float())
)

orders = sqlalchemy.Table(
    "orders", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("customer_id", sqlalchemy.Integer, ForeignKey("customers.id")),
    sqlalchemy.Column("item_id", sqlalchemy.Integer, ForeignKey("items.id")),
    sqlalchemy.Column("date", sqlalchemy.Date()),
    sqlalchemy.Column("status", Enum("open", "paid", "delivered", "closed", name="order_status"))
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


class CustomerIn(BaseModel):
    name: str = Field(max_length=32, title="Name")
    surname: str = Field(max_length=32, title="Surname")
    email: EmailStr = Field(max_length=128, title="Email")
    password: SecretStr = Field(max_length=50, title="Password")


class Customer(CustomerIn):
    id: int


class ItemIn(BaseModel):
    name: str = Field(max_length=50, title="Name")
    description: str = Field(max_length=500, title="Description")
    price: float


class Item(ItemIn):
    id: int


class OrderStatus(str, enum.Enum):
    open = "open"
    paid = "paid"
    delivered = "delivered"
    closed = "closed"


class OrderIn(BaseModel):
    customer_id: int = Field(title="Customer ID")
    item_id: int = Field(title="Item ID")
    date: date
    status: OrderStatus


class Order(OrderIn):
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


@app.get('/fake_data/{count}')
async def create_data(count: int):
    for i in range(count):
        query = customers.insert().values(name=f'Name{i}', surname=f'Surname {i}',
                                          email=f'email{i}@ya.ru', password=f'password{i}')
        await database.execute(query)
        query = items.insert().values(name=f'Name{i}', description=f'Description {i}',
                                      price=i * 1.5)
        await database.execute(query)
        query = orders.insert().values(customer_id=i + 1, item_id=i + 1,
                                       date=datetime.now(), status=OrderStatus.open)
        await database.execute(query)
    return {'message': f'{count} fake things created'}


@app.get('/customers/', response_model=List[Customer])
async def get_customers():
    query = customers.select()
    return await database.fetch_all(query)


@app.get('/customers/{customer_id}', response_model=Customer)
async def get_customer(customer_id):
    query = customers.select().where(customers.c.id == customer_id)
    return await database.fetch_one(query)


@app.post('/add_customer/', response_model=Customer)
async def add_customer(customer: CustomerIn):
    query = customers.insert().values(name=customer.name, surname=customer.surname, email=customer.email,
                                      password=customer.password)
    last_record_id = await database.execute(query)
    return {**customer.dict(), 'id': last_record_id}


@app.put('/update_customer/{customer_id}')
async def update_customer(customer: CustomerIn, customer_id: int):
    query = customers.update().where(customers.c.id == customer_id).values(name=customer.name, surname=customer.surname,
                                                                           email=customer.email,
                                                                           password=customer.password.get_secret_value())
    await database.execute(query)
    return {**customer.dict(), "id": customer_id}


@app.delete('/customers/delete/{customer_id}')
async def delete_customer(customer_id: int):
    query = customers.delete().where(customers.c.id == customer_id)
    await database.execute(query)
    return {"status": f"customer with id {customer_id} is deleted"}


@app.get('/items/', response_model=List[Item])
async def get_items():
    query = items.select()
    return await database.fetch_all(query)


@app.get('/items/{item_id}', response_model=Item)
async def get_itme(item_id):
    query = items.select().where(items.c.id == item_id)
    return await database.fetch_one(query)


@app.post('/add_item/', response_model=Item)
async def add_item(item: ItemIn):
    query = items.insert().values(name=item.name, description=item.description,
                                  price=item.price)
    last_record_id = await database.execute(query)
    return {**item.dict(), 'id': last_record_id}


@app.put('/update_item/{item_id}')
async def update_item(item: ItemIn, item_id: int):
    query = items.update().where(items.c.id == item_id).values(name=item.name, description=item.description,
                                                               price=item.price)
    await database.execute(query)
    return {**item.dict(), "id": item_id}


@app.delete('/items/delete/{item_id}')
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {"status": f"item with id {item_id} is deleted"}


@app.get('/orders/', response_model=List[Order])
async def get_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get('/orders/{order_id}', response_model=Order)
async def get_itme(order_id):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.post('/add_order/', response_model=Order)
async def add_order(order: OrderIn):
    query = orders.insert().values(customer_id=order.customer_id, item_id=order.item_id,
                                   date=order.date, status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), 'id': last_record_id}


@app.put('/update_order/{order_id}')
async def update_order(order: OrderIn, order_id: int):
    query = orders.update().where(orders.c.id == order_id).values(customer_id=order.customer_id, item_id=order.item_id,
                                                                  date=order.date, status=order.status)
    await database.execute(query)
    return {**order.dict(), "id": order_id}


@app.delete('/orders/delete/{order_id}')
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {"status": f"order with id {order_id} is deleted"}
