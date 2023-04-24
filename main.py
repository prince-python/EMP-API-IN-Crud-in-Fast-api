from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app import api as EmpApi

app=FastAPI()
app.include_router(EmpApi.app, tags=["api"])


register_tortoise(
    app,
    db_url="postgres://postgres:root@127.0.0.1/emp",
    modules={'models':['app.models']},
    generate_schemas=True,
    add_exception_handlers=True
)