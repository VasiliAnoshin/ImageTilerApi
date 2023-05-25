
import logging
logger = logging.getLogger(__name__)
from app.tools import Tools
from io import BytesIO
import os

class ImageNotFound(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class DataLoader:
    def __init__(self):
        ...

    @staticmethod
    def get_tiles_by_image_id(user_id:str, image_id: str, tiles:str):
        logger.info('Check if image_id exists and retrieve associated tiles')
        current_deirectory = Tools.get_current_directory(user_id,image_id, tiles)
        if os.path.exists(current_deirectory):
            # Read the saved tile images from disk
            tile_images = []
            # Get all files in the directory
            files = [os.path.join(current_deirectory, f) for f in os.listdir(current_deirectory) if os.path.isfile(os.path.join(current_deirectory, f))]
            for i, tile_path in enumerate(files):
                with open(tile_path, "rb") as f:
                    tile_data = f.read()
                    tile_image = BytesIO(tile_data)
                    tile_images.append({
                        "id":tile_path.split("\\")[-1].split(".")[0],
                        "name":tile_path.split("\\")[-1],
                        "img":tile_image})
            
            return {"tiles": tile_images}
        raise ImageNotFound(status_code=404, detail='Image not found')
    

