# Fastapi 学习笔记

本文主要是fastapi学习相关的笔记。

## Quickstart

一个小demo，用于启动一个类似于hello world的程序。

其中使用fastapi启动程序，然后在main函数中使用uvicorn.run启动web页面，然后我们可以使用get方法来得到一些数据，验证自己的代码。

[代码文件01](../little_demo/fastapi/quickstart.py)

## 路径操作

### 路径操作装饰器

fastapi支持各种请求方法，fastapi使用restful接口规范

|请求方法|
|---|
|@app.get()|
|@app.post()|
|@app.put()|
|@app.patch()|
|@app.delete()|
|@app.get()|
|@app.options()|
|@app.head()|
|@app.trace()|

fastapi路径操作装饰器方法参数

```python
@app.post(
    path="/items/{items_id}",       # URL路径
    response_model=Item,            # 响应模式
    status_code=status.HTTP_200_OK, # HTTP状态码
    tags=["item_tags"],             # docs标签
    summary="item_summary",         # doce简介
    description="item_description", # doce描述
    response_description="item_response_description",   # 响应描述
    deprecated=False                # 是否废弃
)
```

[代码文件0201](../little_demo/fastapi/route_decorator.py)

### 路由分发

通过include_router将路由分发给各个子系统

对于下面系统而言

- apps
- - app1
- - - urls.py
- - - ....py
- - app2
- - - urls.py
- - - ....py
- main.py

我们将这个apps拆分成app1和app2，然后我们在子系统中使用APIRouter，母系统中使用include_router即可实现分发。

其中prefix是路由前缀，不用在子路由里面写。

urls.py
```python
from fastapi import APIRouter

shop = APIRouter()

@shop.get("/food")
def shop_food():
    return {"shop":"food"}

@shop.get("/bed")
def shop_bed():
    return {"shop":"bed"}
```

main.py
```python
from fastapi import FastAPI
import uvicorn

from app1.urls import shop
from app2.urls import user

app = FastAPI

app.include_router(shop,prefix="/shop",tags=["shop接口"])
app.include_router(user,prefix="/user",tags=["user接口"])

if __name__ == '__main__':
    uvicorn.run("main:app")
```

[代码文件0202](../little_demo/fastapi/include_router/main.py)

## 请求与响应

### 路径参数

这里的路径参数指装饰器的参数path，使用与Python格式化字符串相同的语法来声明路径参数或变量。

```python
@app.get("/user/{user_id}")
def get_user(user_id):
    return {"user_id" : user_id}
```

参数的默认类型为str，我们也可以自己指定类型

```python
@app.get("/user/{user_id}")
def get_user(user_id:int):
    return {"user_id" : user_id}
```

同时参数匹配也是有顺序的，会优先匹配先出现的部分。

如下部分id为1时会得到root user而不是1.

```python
@app01.get("/user/1")
def get_user(user_id):
    return {"user_id":"root user"}

@app.get("/user/{user_id}")
def get_user(user_id):
    return {"user_id" : user_id}
```

[代码文件0301](../little_demo/fastapi/request_and_response/apps/app01.py)

### 查询参数

当路径函数中声明了不是路径参数的其它参数时，将会自动解释成查询字符串参数，就是url中?后用&分割的键值对。

```python
@app.get("/jobs/{kd}")
async def search_jobs(kd:str,city:Union[str, None] = None, xl:Optional[str] = None):
    if city or xl
        return {"kd":kd,"city":city,"xl":xl}
    return {"kd":kd}
```

其中city和xl在路径参数"/jobs/{kd}"不存在，它们就被解释为查询参数。

[代码文件0302](../little_demo/fastapi/request_and_response/apps/app02.py)

### 请求体数据

请求体时客户端发给api的数据。响应体时api发给客户端的数据。

FastAPI基于Pydantic，用来做类型强制检查即数据校验。正确时返回值，错误时返回错误信息。

实际传输的数据在http的请求体body中，这里传送的json格式。同时FastApi会自动做部分类型的类型转换。

```python
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
```

[代码文件0303](../little_demo/fastapi/request_and_response/apps/app03.py)

### form表单

FastApi可以使用Form组件接受form表单，用来接收密码流等更适合使用表单字段的内容。

```python
@app04.post("/regin")
async def reg(username:str=Form(),password:str=Form()):
    print(f"username:{username},password:{password}")
    return {"username":username}
```

[代码文件0304](../little_demo/fastapi/request_and_response/apps/app04.py)

### 文件上传

Fastapi可以使用File和UploadFile进行文件上传

```python
@app05.post("/file")
async def get_file(file:bytes = File()):
    print(file)
    return {"file":len(file)}

@app05.post("/files")
async def get_files(files:list[bytes] = File()):
    for file in files:
        print(len(file))
    return {"file":len(files)}

@app05.post("/uploadFile")
async def get_uploadFile(file:UploadFile):
    print(file)
    return {"file":file.filename}

@app05.post("/uploadFiles")
async def get_uploadFiles(files:list[UploadFile]):
    return {"names":[file.filename for file in files]}
```

[代码文件0305](../little_demo/fastapi/request_and_response/apps/app05.py)

### Request对象

有时我们想要直接访问Request对象，获得url、cookie、session、header等信息，我们只需要在函数中声明Request类型参数，Fastapi就会自动传递相关信息进去，让我们获取其中下信息。

```python
@app06.post("/items")
async def items(request:Request):
    return {"URL":request.url,
            "IP":request.client.host,
            "user-agent":request.headers.get("user-agent"),
            "cookies":request.cookies}
```

[代码文件0306](../little_demo/fastapi/request_and_response/apps/app06.py)

### 请求静态文件

不是有web服务器生成的文件为静态文件，如CSS/JS、文件等。

```python
app = FastAPI()
app.mount("/statics",StaticFiles(directory="statics"))
```

运行服务器后就可以在`http://127.0.0.1:8000/statics/`读取对应静态文件

如`http://127.0.0.1:8000/statics/css/common.css`读取/statics/css/common.css文件

### 响应模型参数

#### response_model

之前都是return字典，而FastApi提供了response_model参数，用于声明return的响应体的模型，其为装饰器的参数。

```python
@app.post("/items",response_model=Item)
async def create_item(item:Item):
    ...
```
