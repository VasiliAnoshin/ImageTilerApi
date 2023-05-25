from pydantic import BaseModel
from fastapi import UploadFile, File

class FileUpload(BaseModel):
    file:  UploadFile = File(...)

class TileSizes(BaseModel):
    width: int
    height: int