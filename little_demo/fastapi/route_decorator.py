from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/get')
def get_test():
    return {"method":"get"}

@app.post('/post')
def post_test():
    return {"method":"post"}

@app.put('/put')
def put_test():
    return {"method":"put"}

@app.delete('/delete')
def delete_test():
    return {"method":"delete"}

@app.post('/items',tags=["items接口"],
          summary="items的summary",
          description="items的descrption",
          response_description="items的response descrption")
def test():
    return {"items":"data"}

@app.post('/iitteemmss',deprecated=True)
def tt():
    return {"items":"data"}

if __name__ == '__main__':
    uvicorn.run("route_decorator:app",port=8000,reload=True)