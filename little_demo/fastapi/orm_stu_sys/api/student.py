from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel

from models import *

student_api=APIRouter(prefix="/student")

# 查看所有学生
@student_api.get("/")
async def getAllStudent():
    # students = await Student.all() # 返回 QuarySet类型，类似[Student(),...]
    # for stu in students:
    #     print(stu.name)

    # 过滤查询
    # stus1 = await Student.filter(name="cela") # 过滤查询，返回QuarySet
    # print(stus1[0].id)
    # stu2 = await Student.get(id=2) # 过滤查询，返回对象
    # print(stu2.name)
    # stus3 = await Student.filter(id__gt=1) # 过滤查询id>1
    # stus3 = await Student.filter(id__range=[1,100]) # 过滤查询id范围[1,100]
    # stus3 = await Student.filter(id__in=[1,3,10]) # 过滤查询id在列表[2,3,10]中
    # for stu in stus3:
    #     print(stu.name)

    # values查询
    stus4 = await Student.all().values("id","name") # 返回对应value键值对，[{},{},...]
    # for stu in stus4:
    #     print(stu)

    # 一对多查询
    stu = await Student.get(id=1)
    print(await stu.clas.values('name')) # 获取一个学生对应班级名称
    stus5 = await Student.all().values("name","clas__name") # 查看所有学生班级名称 # clas__name中__为外键查询
    # 多对多
    print(await stu.courses.all().values("name","teacher__name")) # 查询一个学生所有课程
    stus6 = await Student.all().values("name","course__name") # 查看所有学生所有课程名称
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
async def getStudent(id:int):
    stu = await Student.get(id=id)
    return stu

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
    # stu = Student(id=stu_in.id,name=stu_in.name,pwd=stu_in.pwd,clas_id=stu_in.clas_id)
    # await stu.save()
    # 方法2
    stu = await Student.create(id=stu_in.id,name=stu_in.name,pwd=stu_in.pwd,clas_id=stu_in.clas_id)
    # 多对多
    courses = await Course.filter(id__in=stu_in.courses) # 查询学生选课id是否在课程中
    await stu.courses.add(*courses) # *打散
    return stu

# 更新{id}学生
@student_api.put("/{id}")
def updateStudent(id:int):
    return {}

# 删除{id}学生
@student_api.delete("/{id}")
def deleteStudent(id:int):
    return {}