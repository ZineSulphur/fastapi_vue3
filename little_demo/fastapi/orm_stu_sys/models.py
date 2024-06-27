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