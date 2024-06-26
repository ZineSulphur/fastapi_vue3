from fastapi import APIRouter, File, UploadFile

app05 = APIRouter()

@app05.post("/file")
async def get_file(file:bytes = File()):
    print(file)
    return {"file":len(file)}

@app05.post("/files")
async def get_files(files:list[bytes] = File()):
    for file in files:
        print(len(file))
    return {"file":len(files)}

@app05.post("/uploadFile")
async def get_uploadFile(file:UploadFile):
    print(file)
    return {"file":file.filename}

@app05.post("/uploadFiles")
async def get_uploadFiles(files:list[UploadFile]):
    return {"names":[file.filename for file in files]}