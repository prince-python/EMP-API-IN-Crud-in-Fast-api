from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from . models import *
from json import JSONEncoder
from fastapi.encoders import jsonable_encoder

from passlib.context import CryptContext
from fastapi_login.exceptions import InvalidCredentialsException

from fastapi_login import LoginManager
from .pydantic_model import *
import uuid
import typing

app = APIRouter()
SECRET = 'your-secret-key'

manager = LoginManager(SECRET, token_url='/Emp_login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/ragistration_api/")
async def ragistration(data: Employee):
    if await Emp.exists(email=data.email):
        return {"status": False, "message": "email already exists"}
    else:
        user_obj = await Emp.create(email=data.email, name=data.name,
                                     expirence=data.expirence, password=get_password_hash(data.password) ,postion=data.postion,salary=data.salary)
        return user_obj


@manager.user_loader()
async def load_user(email: str):
    if await Emp.exists(email=email):
        user = await Emp.get(email=email)
        return user


@app.post('/login/', )
async def login(data: LoginEmp,
                ):
    email = data.email
    user = await load_user(email)

    if not user:
        return JSONResponse({'status': False, 'message': 'User not Registered'}, status_code=403)
    elif not verify_password(data.password, user.password):
        return JSONResponse({'status': False, 'message': 'Invalid password'}, status_code=403)
    access_token = manager.create_access_token(
        data={'sub': dict({"id": jsonable_encoder(user.id)}), }

    )
    '''test  current user'''
    new_dict = jsonable_encoder(user)
    new_dict.update({"access_token": access_token})
    return Token(access_token=access_token, token_type='bearer')


@app.post("/data/{id}")
async def all_user(data: Get_Person):
    if data.id != 0:
        user = await Emp.get(id=data.id)
        return user
    else:
        user = await Emp.all()
        return user




@app.put("/update/{id}")
async def update(data: Update_Person):
    if await User.filter(email=data.email):
        return {"status":False,"messages":"Email already Exists"}
    elif await User.filter(phone=data.phone):
        return {"status":False,"messages":"Phone number is already Exists"}
    else:
        user = await Emp.create(email=data.email, name=data.name,
                                     expirence=data.expirence, password=get_password_hash(data.password) ,postion=data.postion,salary=data.salary)
        return user


@app.delete("/delete_user/{id}")
async def delete(data: Delete):
    if data.id == 0 or data.id == None or data.id == " ":
        user = await Emp.all().delete()
        return {"status": True, "messages": "all data deleted"}
    else:
        user_obj = await Emp.get(id=data.id).delete()
        return {"status": True, "messages": "user delete"}