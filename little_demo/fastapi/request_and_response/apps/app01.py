from fastapi import APIRouter

app01 = APIRouter()

@app01.get("user/1")
def get_user(user_id):
    return {"user_id":"root user"}

@app01.get("user/{user_id}")
def get_user(user_id):
    return {"user_id":user_id}