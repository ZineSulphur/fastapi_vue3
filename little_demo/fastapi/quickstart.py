from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"user_id":1001}

@app.get("/shop")
def shop():
    return {"shop":123}

if __name__ == '__main__':
    uvicorn.run("quickstart:app",port=8000,reload=True)