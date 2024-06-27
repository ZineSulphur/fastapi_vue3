from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request

from models import *

student_api=APIRouter(prefix="/student")

# 查看所有学生
@student_api.get("/")
async def getAllStudent():
    # students = await Student.all() # 返回 QuarySet类型，类似[Student(),...]
    # for stu in students:
    #     print(stu.name)
    # stus1 = await Student.filter(name="cela") # 过滤查询，返回QuarySet
    # print(stus1[0].id)
    # stu2 = await Student.get(id=2) # 过滤查询，返回对象
    # print(stu2.name)
    # stus3 = await Student.filter(id__gt=1) # 过滤查询id>1
    # stus3 = await Student.filter(id__range=[1,100]) # 过滤查询id范围[1,100]
    # stus3 = await Student.filter(id__in=[1,3,10]) # 过滤查询id在列表[2,3,10]中
    # for stu in stus3:
    #     print(stu.name)
    stus4 = await Student.all().values("id","name") # 返回对应value键值对，[{},{},...]
    # for stu in stus4:
    #     print(stu)
    return stus4

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

# 获得{id}学生
@student_api.get("/{id}")
def getStudent(id:int):
    return {}

# 添加学生
@student_api.post("/")
def addStudent():
    return {}

# 更新{id}学生
@student_api.put("/{id}")
def updateStudent(id:int):
    return {}

# 删除{id}学生
@student_api.delete("/{id}")
def deleteStudent(id:int):
    return {}