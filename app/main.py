from typing import Union
from fastapi import FastAPI, status, HTTPException, File, UploadFile
from app.Image import PanoramicImage
from app.log import *
app = FastAPI()

logger = logging.getLogger(__name__)

@app.post("/upload_panoramic_image", tags=["Image"], status_code=status.HTTP_200_OK)
def upload_panoramic_image(file: UploadFile = File(...)):
    try:
        logger.debug('Start upload panoramic image process ....')
        if file is None:
            raise HTTPException(status_code=400, detail='No file found')
        img = PanoramicImage(file) 
        img.upload_image()       
        #Add format check.
        #Check that file is not infected and maxfile size image is valid
        #Generate image id and provide to user
        logger.debug('Upload panoramic image process completed ....')
        return {'message': 'Image uploaded successfully'}
    except Exception as ex:
        logger.info(f'Unexpected error.  Exception: {ex.args[0]} ')
        raise HTTPException(status_code=500, detail=ex.args[0])


@app.get("/get_tiled_images", tags=["Image"], status_code=status.HTTP_200_OK)
def get_tiled_images():
    try:
        ...
    except Exception as ex:
        logger.info(f'Unexpected error.  Exception: {ex.args[0]} ')
        raise HTTPException(status_code=500, detail=ex.args[0])