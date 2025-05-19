import base64
from typing import Annotated
from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse
from starlette.templating import Jinja2Templates
import os
import shutil
import uuid
import aiofiles
import json
from Api3D import chatGeneration, imageGeneration, modelGeneration
app = FastAPI()

MODEL_DIR = "photo"
app.mount("/photo", StaticFiles(directory=MODEL_DIR), name="photo")
UPLOAD_DIRECTORY = '/photo/'
@app.get('/')
def root():
    return {'ok':'200'}

@app.post("/3d")
async def modelGen(file: UploadFile = File(...), hf_token: Annotated[list[str] | None, Header()] = None):
    contents = await file.read()
    with open(f'{file.filename}', 'wb') as f:
        f.write(contents)
    pathFile = await modelGeneration(photo=file.filename, token=hf_token[0])
    print(file.filename[0:-3])

    with open(pathFile, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('ascii')
        stringCoded = str(encoded_string)
        print(stringCoded)
    jsonR = json.dumps({'bytes': encoded_string}, ensure_ascii=False).encode("utf-8")
    print(pathFile)
    return Response(content=jsonR, media_type="application/json")
    

@app.post("/image")
async def imageGen(promt: Annotated[list[str] | None, Header()] = None, token: Annotated[list[str] | None, Header()] = None):
    res = {}
    print(promt)
    res = await imageGeneration(promt=promt[0], token=token[0])
    listBase64 = []
    for i in range(4):
        path = res[i]['image']
        with open(path, 'rb') as file:
            encoded_string = base64.b64encode(file.read()).decode('ascii')
            stringCoded = str(encoded_string)
            listBase64.append(stringCoded)

    jsonR = json.dumps({'0': listBase64[0],'1': listBase64[1],'2': listBase64[2],'3': listBase64[3]})
    return Response(content=jsonR, media_type="application/json")

@app.post("/chat")
async def chatRequest(promt: Annotated[list[str] | None, Header()] = None, token: Annotated[list[str] | None, Header()] = None):
    res = await chatGeneration(promt=promt, token=token) #!######
    jsonR = json.dumps({'0': res})
    return Response(content=jsonR, media_type="application/json")