from pydantic import BaseModel

class Employee(BaseModel):
    name:str
    email:str
    password:str
    salary:int
    expirence:int
    postion:str
    
    
    
    
    
class LoginEmp(BaseModel):
    email:str
    password:str
    
class Token (BaseModel):
    access_token: str
    token_type: str= 'bearer'
    
    
    
    
class Delete(BaseModel):
    id:int

class Get_Person(BaseModel):
    id:int

class Update_Person(BaseModel):
    id:int
    name:str
    email:str
    password:str
    salary:int
    expirence:int
    postion:str