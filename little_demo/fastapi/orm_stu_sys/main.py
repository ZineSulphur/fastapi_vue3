from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise

from settings import TORTOISE_ORM
from api.student import student_api

app = FastAPI()

app.include_router(student_api)

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    # generate_schemas=True, # 如果数据库/schema为空，自动创建数据库/schema，生产环境一般不开
    # add_exception_handlers=True, # 生产环境不开，会泄露调试信息
)

if __name__ == '__main__':
    uvicorn.run("main:app")