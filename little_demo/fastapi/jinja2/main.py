from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/index")
def index(request:Request):
    name = "root"
    age = 32
    books = ["聊斋","书","好多书"]
    person = {"name":"a","age":12,"gender":"male"}
    pi = 3.1415926
    return templates.TemplateResponse(
        "index.html", # 模板文件
        {
            "request":request,
            "user":name,
            "age":age,
            "books":books,
            "person":person,
            "pi":pi
        } # context上下文对象
    )

if __name__ == '__main__':
    uvicorn.run("main:app")