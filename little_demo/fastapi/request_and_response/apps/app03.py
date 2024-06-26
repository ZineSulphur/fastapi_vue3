from datetime import date
from typing import Optional, Union
from fastapi import APIRouter
from pydantic import BaseModel,Field, field_validator

app03 = APIRouter()

class User(BaseModel):
    # 带默认值，也可以不指定默认值
    # name:str = "root"
    name:str
    age:int = Field(default=0,gt=0,lt=100) # Field 指定字段规则
    birth:Union[date, None] = None
    friends:list[int] = []
    description:Optional[str] = None

    # 校验name为字母
    @field_validator("name")
    def name_must_alpha(cls, value):
        assert value.isalpha(),'name must be alpha'
        return value
    
class Data(BaseModel):
    # 嵌套User
    data:list[User]

@app03.post("/user")
async def user(user:User):
    print(user, type(user))
    print(user.name)
    print(user.model_dump())
    return user

@app03.post("/data")
async def data(data:Data):
    return data