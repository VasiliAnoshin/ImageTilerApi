from pydantic import BaseModel
from fastapi import UploadFile, File

class FileUpload(BaseModel):
    file:  UploadFile = File(...)

class TileSizes(BaseModel):
    width: int
    height: int

class UserRequest(BaseModel):
    user_id: str
    image_id:str
    tiles: list