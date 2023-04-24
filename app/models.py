from tortoise.models import Model
from tortoise import Tortoise , fields


class Emp(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(200)
    email=fields.CharField(400)
    password = fields.CharField(300)
    salary=fields.CharField(100)
    expirence=fields.CharField(50)
    postion=fields.CharField(100)
   
    
Tortoise.init_models(['app.models'],'models')
