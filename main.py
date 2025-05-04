import base64
from typing import Annotated
from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from tkinter.font import names
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
from Api3D import generate3d
app = FastAPI()

MODEL_DIR = "photo"
app.mount("/photo", StaticFiles(directory=MODEL_DIR), name="photo")
UPLOAD_DIRECTORY = '/photo/'
@app.get('/')
def root():
    return {'ok':'200'}

@app.post("/add")
async def upload_file(file: UploadFile = File(...), hf_token: Annotated[list[str] | None, Header()] = None):
    print(hf_token[0])
    print(hf_token)
    contents = await file.read()
    with open(f'{file.filename}', 'wb') as f:
        f.write(contents)
    pathFile = await generate3d(photo=file.filename, token=hf_token[0])
    print(file.filename[0:-3])

    with open(pathFile, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('ascii')
        stringCoded = str(encoded_string)
        print(stringCoded)
    jsonR = json.dumps({'bytes': encoded_string}, ensure_ascii=False).encode("utf-8")
    print(pathFile)
    return Response(content=jsonR, media_type="application/json")
    