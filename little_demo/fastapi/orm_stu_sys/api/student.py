from fastapi import APIRouter

student_api=APIRouter(prefix="/student")

# 查看所有学生
@student_api.get("/s")
def getAllStudent():
    return {}

# 添加学生
@student_api.post("/")
def addStudent():
    return {}

# 获得{id}学生
@student_api.get("/{id}")
def getStudent(id:int):
    return {}

# 更新{id}学生
@student_api.put("/{id}")
def updateStudent(id:int):
    return {}