# Fastapi 学习笔记

本文主要是fastapi学习相关的笔记。

## Quickstart

一个小demo，用于启动一个类似于hello world的程序。

其中使用fastapi启动程序，然后在main函数中使用uvicorn.run启动web页面，然后我们可以使用get方法来得到一些数据，验证自己的代码。

[code](../little_demo/fastapi/quickstart.py)

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

[code](../little_demo/fastapi/route_decorator.py)

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
