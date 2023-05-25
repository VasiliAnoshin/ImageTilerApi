from typing import Union
from fastapi import FastAPI, status, HTTPException
import logging
app = FastAPI()

logger = logging.getLogger(__name__)

@app.post("/upload_panoramic_image", tags=["Image"], status_code=status.HTTP_200_OK)
def upload_panoramic_image():
    try:
        ...
    except Exception as ex:
        logger.info(f'Unexpected error.  Exception: {ex.args[0]} ')
        raise HTTPException(status_code=500, detail=ex.args[0])


@app.get("/get_tiled_images", tags=["Image"], status_code=status.HTTP_200_OK)
def read_item():
    try:
        ...
    except Exception as ex:
        logger.info(f'Unexpected error.  Exception: {ex.args[0]} ')
        raise HTTPException(status_code=500, detail=ex.args[0])