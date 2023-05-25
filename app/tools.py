import uuid
import logging
import os
import re

logger = logging.getLogger(__name__)

class Tools:
    def __init__(self):
        ...
    
    @staticmethod
    def genrate_image_id(user_id:int)->str:
        logger.info('Generate image id that will be used as identificator for image.')
        return str(f'{user_id}_{uuid.uuid4()}')
    
    @staticmethod
    def allowed_file(file_name:str) -> bool:
        logger.info('Check for provided file format in the jpg, jpeg, png')
        return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}
    
    @staticmethod
    def is_valid_tiles_format(tiles: str) -> bool:
        """
        Checks if the given tiles format is valid.

        Args:
            tiles (str): The tiles format to check.

        Returns:
            bool: True if the format is valid, False otherwise.
        """
        pattern = r"^\d+x\d+$"
        return re.match(pattern, tiles) is not None

    @staticmethod
    def get_current_directory(user_id:str, image_id:str, tiles:str) -> str:
        """
        Constructs the current directory path based on the user ID, image ID, and tiles format.

        Args:
            user_id (str): The ID of the user.
            image_id (str): The ID of the image.
            tiles (str): The tiles format.

        Returns:
            str: The current directory path.
        """
        if not user_id:
            raise ValueError('user_id cant be empty')
        if not image_id:
            raise ValueError('image_id cant be empty')
        if not tiles:
            raise ValueError('tiles cant be empty')
        if not Tools.is_valid_tiles_format(tiles):
            raise Exception('Provided tiles not in correct format. Correct example: 256x256')
        tils = str(f'{tiles} tiles')
        cur_dir = os.path.join(os.getcwd(), "app", "Data", f"{user_id}", image_id, tils)
        return cur_dir