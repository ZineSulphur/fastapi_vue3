from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# @app.middleware('http')
# async def CORSMiddleware(request:Request, call_next):
#     response = await call_next(request)
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response

orgins = ['http://localhost:8000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=orgins, # '*':表示所有客户端,[]为客户端列表
    allow_credentials=True,
    allow_methods=['GET','POST'],
    allow_headers=['*'],
)

@app.get('/user')
def get_user():
    print('get_user run')
    return {
        'user':'current user'
    }

if __name__ == '__main__':
    uvicorn.run("main:app")