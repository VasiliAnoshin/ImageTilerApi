
import logging
logger = logging.getLogger(__name__)
from app.tools import Tools
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
            return True
        raise ImageNotFound(status_code=404, detail='Image not found')
    

