
import logging
logger = logging.getLogger(__name__)
from app.tools import Tools
import os
import io
import zipfile


class ImageNotFound(Exception):
    def __init__(self, status_code:int, detail:str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class DataLoader:
    def __init__(self):
        ...

    @staticmethod
    def get_tiles_by_image_id(user_id:str, image_id: str, tiles:str)->io.BytesIO():
        """
        Retrieve associated tiles for the specified `image_id` belonging to the given `user_id` and package them into a ZIP file.

        Args:
            user_id (str): The ID of the user.
            image_id (str): The ID of the image.
            tiles (str): The directory containing the tile images.

        Returns:
            Optional[io.BytesIO]: zip file

        Raises:
            ImageNotFound: If the `image_id` does not exist.
        """
        logger.info('Check if image_id exists and retrieve associated tiles')
        current_directory = Tools.get_current_directory(user_id, image_id, tiles)
        if os.path.exists(current_directory):
            # Create an in-memory byte stream to hold the ZIP file contents
            zip_data = io.BytesIO()
            with zipfile.ZipFile(zip_data, "w") as zip_file:
                # Get all files in the directory
                files = [os.path.join(current_directory, f) for f in os.listdir(current_directory) if
                        os.path.isfile(os.path.join(current_directory, f))]
                for i, tile_path in enumerate(files):
                    with open(tile_path, "rb") as f:
                        tile_data = f.read()
                        # Add each file to the ZIP archive
                        zip_file.writestr(f"{i}.png", tile_data)

            return zip_data
        raise ImageNotFound(status_code=404, detail='Image not found')

