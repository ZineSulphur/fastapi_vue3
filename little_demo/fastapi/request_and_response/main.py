from fastapi import FastAPI
import uvicorn

from apps.app01 import app01
from apps.app02 import app02
from apps.app03 import app03
from apps.app04 import app04

app = FastAPI()

app.include_router(app01,tags=["app01路径参数"])
app.include_router(app02,tags=["app02查询参数"])
app.include_router(app03,tags=["app03请求体数据"])
app.include_router(app04,tags=["app04form表单"])

if __name__ == '__main__':
    uvicorn.run("main:app")