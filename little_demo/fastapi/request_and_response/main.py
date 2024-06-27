from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from apps.app01 import app01
from apps.app02 import app02
from apps.app03 import app03
from apps.app04 import app04
from apps.app05 import app05
from apps.app06 import app06
from apps.app07 import app07

app = FastAPI()

app.mount("/statics",StaticFiles(directory="statics"))

app.include_router(app01,tags=["app01路径参数"])
app.include_router(app02,tags=["app02查询参数"])
app.include_router(app03,tags=["app03请求体数据"])
app.include_router(app04,tags=["app04form表单"])
app.include_router(app05,tags=["app05文件"])
app.include_router(app06,tags=["app06request对象"])
app.include_router(app07,tags=["app07响应参数"])

if __name__ == '__main__':
    uvicorn.run("main:app")