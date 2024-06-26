from fastapi import FastAPI
import uvicorn

from app1.urls import shop
from app2.urls import user

app = FastAPI()

app.include_router(shop,prefix="/shop",tags=["shop接口"])
app.include_router(user,prefix="/user",tags=["user接口"])

if __name__ == '__main__':
    uvicorn.run("main:app")