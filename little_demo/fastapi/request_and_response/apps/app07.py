from typing import Union
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

app07 = APIRouter()

class UserIn(BaseModel):
    username:str
    password:str
    email:EmailStr
    full_name:Union[str,None]=None

class UserOut(BaseModel):
    username:str
    email:EmailStr
    full_name:Union[str,None]=None

@app07.post("/user2",response_model=UserOut) # 指定输出类型为UserOut
def create_user(user:UserIn):
    # 数据库业务操作#
    return user

class Item(BaseModel):
    name:str
    description:Union[str,None]=None
    price:float
    tax:float=10.5
    tags:list[str]=[]

items = {
    "foo":{"name":"Foo","price":50.2},
    "bar":{"name":"Bar","description":"The bartenders","price":62,"tax":20.2},
    "baz":{"name":"Baz","description":None,"price":50.2,"tax":10.5,"tags":[]}
}

@app07.get("/items/{item_id}",response_model=Item,response_model_exclude_unset=True)
async def read_item(item_id:str):
    return items[item_id]

@app07.get("/items2/{item_id}",response_model=Item,response_model_exclude={"description"})
async def read_item2(item_id:str):
    return items[item_id]

@app07.get("/items3/{item_id}",response_model=Item,response_model_include={"name","price"})
async def read_item3(item_id:str):
    return items[item_id]