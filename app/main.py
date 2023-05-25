from typing import Union
from fastapi import FastAPI, status, HTTPException, File, UploadFile, Form, Response
from app.image import PanoramicImage
from app.log import *
from app.tools import Tools
from typing import Optional, List, Tuple
from app.schemas import TileSizes, UserRequest
from app.data_loader import DataLoader
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

#<TODO>Check that file is not infected and maxfile size image is valid. tile_sizes: List[TileSizes],
@app.post("/upload_panoramic_image", tags=["Image"], status_code=status.HTTP_200_OK)
def upload_panoramic_image(file: UploadFile = File(...), 
                           user_id: str = Form("user_id")):
    """
    Uploads a panoramic image in following format jpg, jpeg, png.

    ---------------
    Args:
    ----------------
        file (UploadFile): The panoramic image file to upload.
        user_id (str): The ID of the user associated with the image.
    
    ---------------
    Returns:
    ----------------
        dict: A dictionary containing the success message, image ID, and user ID.

    ---------------
    Raises:
    ----------------
        HTTPException: If an unexpected error occurs during the upload process.
    """
    try:
        logger.debug('Start upload panoramic image process ....')
        image_id = Tools.genrate_image_id(user_id)
        img = PanoramicImage(file, image_id, user_id, [(256,256)])
        img.upload_image_handler()       
        logger.debug('Upload panoramic image process completed ....')
        return {'message': 'Image uploaded successfully', 'image_id': image_id, 'user_id': user_id}
    except Exception as ex:
        logger.info(f'Unexpected error.  Exception: {ex.args[0]} ')
        raise HTTPException(status_code=500, detail=ex.args[0])


@app.get("/get_tiled_images", tags=["Image"], status_code=status.HTTP_200_OK)
def get_tiled_images(user_id:str, image_id:str, tiles:str):
    """
    Retrieves the tiled images based on the user ID, image ID, and tiles format.
    
    ---------------
    Args:
    ---------------
        user_id (str): The ID of the user.
        image_id (str): The ID of the image.
        tiles (str): The tiles format.
    ---------------
    Returns:
    ---------------
        zip_file with tiled images
    ---------------
    Raises:
    ---------------
        HTTPException
    --------------- 
    Example:
    ---------------
        get_tiled_images("123", "image_1", "256x256")

    """
    try:
        logger.debug(f'Tiled images request ... img_id: {image_id}, user_id: {user_id}, tiles: {tiles}')
        zip_data= DataLoader.get_tiles_by_image_id(user_id=user_id, image_id=image_id, tiles=tiles)
        # Return the ZIP file data and headers
        response = Response(
            content=zip_data.getvalue(), 
            headers={
            "Content-Type": "application/zip",
            "Content-Disposition": f"attachment; filename=tiles.zip"})
        return response
    except Exception as ex:
        logger.info(f'Unexpected error.  Exception: {ex.args[0]}')
        raise HTTPException(status_code=500, detail=ex.args[0])