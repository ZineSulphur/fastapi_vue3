import time
from fastapi import FastAPI, Request, Response
import uvicorn

app = FastAPI()

@app.middleware('http')
async def m2(request:Request,call_next):
    # 请求
    print('m2 request')
    response = await call_next(request)
    # 响应
    response.headers['author']='abc' # header 中添加author字段
    print('m2 response')
    return response

@app.middleware('http')
async def m1(request:Request,call_next):
    # 请求
    print('m1 request')
    # if request.client.host in ['127.0.0.1']: # 黑名单，127.0.0.1的用户不能访问
    #     return Response(status_code=403,content='visit forbidden') # 直接返回响应体
    # if request.url.path in ['/user']: # 指定路径，/user路径不能访问，常用于权限
    #     return Response(status_code=403,content='visit forbidden') # 直接返回响应体
    start = time.time()
    response = await call_next(request)    
    # 响应
    print('m1 response')
    end = time.time()
    response.headers['ProcessTime']=str(end-start) # 计算运行时间
    return response

@app.get('/user')
def get_user():
    time.sleep(2)
    print('get_user run')
    return {
        'user':'current user'
    }

@app.get('/user/{item_id}')
def get_item(item_id:int):
    time.sleep(1)
    print('get_item run')
    return {
        'item_id':item_id
    }

if __name__ == '__main__':
    uvicorn.run("main:app")