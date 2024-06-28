# Fastapi 学习笔记

本文主要是fastapi学习相关的笔记。

## Quickstart

一个小demo，用于启动一个类似于hello world的程序。

其中使用fastapi启动程序，然后在main函数中使用uvicorn.run启动web页面，然后我们可以使用get方法来得到一些数据，验证自己的代码。

[quickstart代码](../little_demo/fastapi/quickstart.py)

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

[路径操作装饰器代码](../little_demo/fastapi/route_decorator.py)

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

shop = APIRouter() # APIRouter() 参数中也可以使用prefix参数

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

[路由分发代码](../little_demo/fastapi/include_router/main.py)

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

[路径参数代码](../little_demo/fastapi/request_and_response/apps/app01.py)

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

[查询参数代码](../little_demo/fastapi/request_and_response/apps/app02.py)

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

[请求体代码](../little_demo/fastapi/request_and_response/apps/app03.py)

### form表单

FastApi可以使用Form组件接受form表单，用来接收密码流等更适合使用表单字段的内容。

```python
@app04.post("/regin")
async def reg(username:str=Form(),password:str=Form()):
    print(f"username:{username},password:{password}")
    return {"username":username}
```

[form代码](../little_demo/fastapi/request_and_response/apps/app04.py)

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

[文件上传代码](../little_demo/fastapi/request_and_response/apps/app05.py)

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

[request代码](../little_demo/fastapi/request_and_response/apps/app06.py)

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

Fastapi将使用response_model参数来声明用于响应的模型

- 将输出转换为response_model中声明的数据类型
- 验证数据结构和类型
- 将输出数据类型限制为定义的类型
- 添加到Openapi中
- 在自动文档中使用response_model

```python
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
```

以上的输出会比输入少password

#### response_model_exclude_unset

Fastapi可以利用`response_model_exclude_unset`参数来忽略返回的结果。即忽略有默认值时不返回默认值的结果。

```python
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

@app07.get("/otems/{item_id}",response_model=Item,response_model_exclude_unset=True)
async def read_item(item_id:str):
    return items[item_id]
```

response_model_exclude_unset=False时，输入foo返回
```{"name":"Foo","description":None,"price":50.2,"tax":10.5,"tags":[]}```

response_model_exclude_unset=True时，输入foo返回
```"foo":{"name":"Foo","price":50.2}```

即response_model_exclude_unset=True时，返回的响应体中只有修改的部分返回，没有修改和默认值的部分被排除了。

此外还有`response_model_exclude_defaults`和`response_model_exclude_none`参数用于排除默认值和None值。

#### include & exclude

`response_model_include`和`response_model_exclude`参数用于在响应体中包含和排除某些字段。

设置`response_model_include`时响应体只包含设置的字段。

设置`response_model_exclude`时响应体会排除设置的字段。

```python
@app07.get("/items2/{item_id}",response_model=Item,response_model_exclude={"description"})
async def read_item2(item_id:str):
    return items[item_id]

@app07.get("/items3/{item_id}",response_model=Item,response_model_include={"name","price"})
async def read_item3(item_id:str):
    return items[item_id]
```

[响应模型参数代码](../little_demo/fastapi/request_and_response/apps/app07.py)

## jinja2模板

模板简单来说就是一个其中包含占位变量表示动态部分的文件，模板文件在经过动态赋值后，返回给用户。

jinja2是Flask作者开发的一个模板系统，起初是仿django模板，由于其灵活快速和安全等优点被广泛使用。

jinja2主要语法

1. 变量 `{{ }}`
2. 控制结构 `{% %}`
3. 过滤器 `{{|}}`
4. 注释 `{# #}`

### 变量

jinja2模板会替换html等模板文件中的{{ xxx }}内容作为变量，同时可以使用{{ xxx.xx }}来读取列表和字典等变量的值。

```python
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/index")
def index(request:Request):
    name = "root"
    age = 32
    books = ["聊斋","书","好多书"]
    person = {"name":"a","age":12,"gender":"male"}
    return templates.TemplateResponse(
        "index.html", # 模板文件
        {
            "request":request,
            "user":name,
            "age":age,
            "books":books,
            "person":person
        } # context上下文对象
    )
```

templates/html模板文件中的内容
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<p>用户名：{{ user }}</p>
<p>年龄：{{ age }}</p>
<p>一些书：{{ books }}</p>
<ul>
    <li>第一本书：{{ books.0 }}</li>
    <li>第二本书：{{ books.1 }}</li>
    <li>第三本书：{{ books.2 }}</li>
</ul>
<p>一个人：{{ person }}</p>
<p>姓名：{{ person.name }}</p>
<p>年龄：{{ person.age }}</p>
<p>性别：{{ person.gender }}</p>
</body>
</html>
```

### 过滤器

变量可以通过过滤器进行修改，过滤器可以认为是jinja2的内置函数和字符串处理函数。

常用过滤器有：

|过滤器|说明|
|---|---|
|capitialize|首字母大小|
|upper|转换成大写|
|lower|转换成小写|
|title|每个单词首字母大写|
|trim|去除首尾空格|
|striptags|渲染前删除值中的HTML标签|
|join|拼接字符串|
|round|默认四舍五入，可以用参数控制|
|safe|渲染时值不转义|

在使用时只需要使用管道|即可使用过滤器

```jinja
{{ 'abc'| catialize }} # Abc
{{ 'abc'| upper }} # ABC
{{ 'hello world'| title }} # Hello World
{{ 'hello world'| replace('world','there') | upper }} # HELLO THERE
{{ 18.18 | round | int }} # 18
```

### 控制结构

#### 分支

jinja2的if分支结构

```jinja
{% if xxx %}
    ...
{% else %}
    ...
{% endif %}
```

#### 循环

jinja2的for循环结构

```jinja
{% for book in books %}
    <p>{{ book }}</p>
{% endfor %}
```

[jinja2模板代码](../little_demo/fastapi/jinja2/main.py)
[jinja2模板](../little_demo/fastapi/jinja2/templates/index.html)

## ORM

对象关系映射（英语：Object Relational Mapping，简称ORM，或O/RM，或O/R mapping），是一种程序技术，用于实现面向对象编程语言里不同类型系统的数据之间的转换。从效果上说，它其实是创建了一个可在编程语言里使用的--“虚拟对象数据库”。

Fastapi也可以使用ORM技术来对数据库进行操作，目前主要使用的ORM有SQLAlchemy和TortoiseORM等。

这里主要使用TortoiseORM。

安装TortoiseORM

```bash
pip install tortoise-orm

# 安装数据库驱动
pip install tortoise-orm[asyncpg]   # pg
pip install tortoise-orm[aiomysql]  # mysql
pip install tortoise-orm[asyncmy]   # mysql
# 除此之外，还支持：aiosqlite
```

### 创建模型

其实就是将数据模型中的表和关系等，以ORM类的方式表示出来

以选课系统为例

```python
from tortoise.models import Model
from tortoise import fields

class Student(Model):
    id = fields.IntField(pk=True,description="学号") # 主键
    name = fields.CharField(max_length=32, description="姓名")
    pwd = fields.CharField(max_length=32, description="密码")
    # 一对多
    clas = fields.ForeignKeyField(model_name="models.Clas",related_name="strudents") # 外键
    # 多对多
    courses = fields.ManyToManyField(model_name="models.Course",related_name="strudents")

class Clas(Model):
    id = fields.IntField(pk=True) # 主键
    name = fields.CharField(max_length=32, description="班级名称")

class Course(Model):
    id = fields.IntField(pk=True) # 主键
    name = fields.CharField(max_length=32, description="课程名称")
    
    teacher = fields.ForeignKeyRelation(model_name="models.Teacher",related_name="strudents") # 外键

class Teacher(Model):
    id = fields.IntField(pk=True) # 主键
    name = fields.CharField(max_length=32, description="姓名")
    pwd = fields.CharField(max_length=32, description="密码")
```

[ORM模型代码](../little_demo/fastapi/orm_stu_sys/models.py)

### aerich迁移工具

首先准备tortoiseorm配置文件和主函数

配置文件setting.py
```python
TORTOISE_ORM={
        'connections':{# 数据库连接配置
            'default':{
                'engine':'tortoise.backends.mysql', #mysql
                # 'engine':'tortoise.backends.asyncpg', #pg
                'credentials':{
                    'host':'127.0.0.1',
                    'port':'3306',
                    'user':'root',
                    'password':'root',
                    'database':'fastapi_learn',
                    'minsize':1,
                    'maxsize':5,
                    'charset':'utf8mb4',
                    'echo':True
                }
            }
        },
        'apps':{
            'models':{
                'models':['models','aerich.models',], # 加载模组类，aerich迁移还需要加'aerich.models'
                'default_connection':'default' 
            }
        },
        'use_tz':False,
        'timezone':'Asia/Shanghai'
    }
```

main.py
```python
from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise

from settings import TORTOISE_ORM

app = FastAPI()

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    # generate_schemas=True, # 如果数据库/schema为空，自动创建数据库/schema，生产环境一般不开
    # add_exception_handlers=True, # 生产环境不开，会泄露调试信息
)

if __name__ == '__main__':
    uvicorn.run("main:app")
```

aerich是一种ORM迁移工具，需结合tortoise框架使用。

安装aerich

```bash
pip install aerich
```

#### 1. 初始化配置（只需要使用一次）

```bash
aerich init -t settings.TORTOISE_ORM # TORTOISE_ORM配置文件位置
```

在settings.py文件也就是配置的文件目录下执行。

初始化完成后生成pyproject.toml文件和migrations文件夹
- pyproject.toml 保存配置文件路径
- migrations 存放迁移文件

#### 2. 初始化数据库（一般只需要使用一次）

```bash
aerich init-db
```

初始化数据库之后，会在数据库中生成对应的表。

如果TORTOISE_ORM配置文件中的models改了名，则执行这条命令的时候需要加上`--app`参数，来指定修改的地方。

#### 3. 更新模型并进行迁移

首先修改model类，重新生成迁移文件，比如添加一个字段
```python
class xxx(Model):
    ...
    xxx = fields.CharField(max_length=255)
```
```bash
aerich migrate [--name] (标记修改操作)

aerich migrate
或者
aerich migrate --name add_column
```
执行aerich migrate之后会在migrations中生成对应文件

之后执行upgrade/downgrade来应用/撤回数据库中的更改

```bash
# 升级
serich upgrade
# 降级
serich downgrade
```

#### 4. 查看历史记录

```bash
aerich history
```

### ORM增删改查

#### API接口

应用程序编程接口（英语：Application Programming Interface，简称：API），是一些预先定义的函数，目的是提供应用程序与开发人员基于某软件或硬件得以访问一组例程的能力，而又无需访问源码，或理解内部工作机制的细节。

即应用程序对外提供的一个执行程序的入口。

#### RESTful规范

REST全称是Representational State Transfer，通常译为表征性状态转移。 

RESTful是一种定义Web API接口的设计风格，尤其适用于前后端分离的应用模式中。

这种风格的理念认为后端开发任务就是提供数据的，对外提供的是数据资源的访问接口，所以在定义接口时，客户端访问的URL路径就表示这种要操作的数据资源。事实上，我们可以使用任何一个框架都可以实现符合restful规范的API接口。

简单来说就是客户端和服务器交互的时候，使用HTTP的不同请求方法代表不同动作

- GET 获取资源
- POST 新建资源
- PUT 更新资源
- DELETE 删除资源

而对学生系统，其相关内容可以如下表示。

|请求方法|请求地址|操作|
|---|---|---|
|GET|/students|获取所有学生|
|POST|/students|增加学生|
|GET|/strdents/1|获取编号为1的学生|
|PUT|/strdents/1|修改编号为1的学生|
|DELETE|/strdents/1|删除编号为1的学生|

其它规范参考下文

[Restful规范](https://www.cnblogs.com/97zs/p/18146070)

#### 接口开发

根据上面的RESTful规则进行开发

```python
from fastapi import APIRouter

student_api=APIRouter(prefix="/student")

# 查看所有学生
@student_api.get("/")
def getAllStudent():
    ...
    return {}
...
```

##### ORM查询

```python
from models import * # import ORM类

students = await Student.all() # 返回 QuarySet类型，类似[Student(),...]
for stu in students:
    print(stu.name)

stus1 = await Student.filter(name="cela") # 过滤查询，返回QuarySet
print(stus1[0].id)

stu2 = await Student.get(id=2) # 过滤查询，返回对象
print(stu2.name)

stus3 = await Student.filter(id__gt=1) # 过滤查询id>1
stus3 = await Student.filter(id__range=[1,100]) # 过滤查询id范围[1,100]
stus3 = await Student.filter(id__in=[1,3,10]) # 过滤查询id在列表[2,3,10]中
for stu in stus3:
    print(stu.name)

stus4 = await Student.all().values("id","name") # 返回对应value键值对，[{},{},...]
for stu in stus4:
    print(stu)
```

而对于用jinja2前端的响应体，我们可以这么写

```python
@student_api.get("/index.html")
async def getAllStudent(request:Request):
    templates = Jinja2Templates(directory="templates")
    students = await Student.all()
    return templates.TemplateResponse(
        "index.html",{
            "request":request,
            "students":students
        }
    )
```

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!-- 最新版本的 Bootstrap 核心 CSS 文件 -->
    <link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
</head>
<body>
    <h1>学生信息</h1>

    <div class="row">
        <div class="col-md-9">
            <table class="table table-bordered table-striped table-hover">
                <thead>
                    <tr>
                        <th>学生学号</th>
                        <th>学生姓名</th>
                        <th>学生班级</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in students %}
                    <tr>
                        <td>{{ student.id }}</td>
                        <td>{{ student.name }}</td>
                        <td>{{ student.clas_id }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
```

##### 添加表记录

使用ORM模型类的create方法进行SQL的Insert操作。

```python
# 输入学生信息类
class StudentIn(BaseModel):
    id:int
    name:str
    pwd:str
    clas_id:int
    courses:list[int]=[]

# 添加学生
@student_api.post("/")
async def addStudent(stu_in:StudentIn):
    # 插入数据库
    # 方法1
    stu = Student(id=stu_in.id,name=stu_in.name,pwd=stu_in.pwd,clas_id=stu_in.clas_id)
    await stu.save()
    # 方法2
    stu = await Student.create(id=stu_in.id,name=stu_in.name,pwd=stu_in.pwd,clas_id=stu_in.clas_id)
    return stu
```

##### 多对多查询添加

在插入之后，我们发现虽然student表中有新增内容，但是多对多表student_course中没有新增信息，所以我们也需要在里面新增信息。

```python
# 添加学生
@student_api.post("/")
async def addStudent(stu_in:StudentIn):
    # 插入数据库
    stu = await Student.create(id=stu_in.id,name=stu_in.name,pwd=stu_in.pwd,clas_id=stu_in.clas_id)
    # 多对多
    courses = await Course.filter(id__in=stu_in.courses) # 查询学生选课id是否在课程中
    await stu.courses.add(*courses) # *打散
    return stu
```

查询

```python
# 一对多查询
    stu = await Student.get(id=1)
    print(await stu.clas.values('name')) # 获取一个学生对应班级名称
    stus5 = await Student.all().values("name","clas__name") # 查看所有学生班级名称 # clas__name中__为外键查询
    # 多对多
    print(await stu.courses.all().values("name","teacher__name")) # 查询一个学生所有课程
    stus6 = await Student.all().values("name","course__name") # 查看所有学生所有课程名称
```

##### 编辑接口

