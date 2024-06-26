from fastapi import APIRouter
from typing import Optional, Union

app02 = APIRouter()

@app02.get("/jobs/{kd}")
async def get_jobs(kd:str, xl:Union[str,None]=None, gj:Optional[str]=None):
    # 基于kd, xl, gj查询query
    return {"kd":kd,"xl":xl,"gj":gj}