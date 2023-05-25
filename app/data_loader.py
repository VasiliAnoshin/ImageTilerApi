
import logging
logger = logging.getLogger(__name__)
from app.tools import Tools
from io import BytesIO
import os
import io
import zipfile
from fastapi import FastAPI, Response
import gzip

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
                        # tile_image = BytesIO(tile_data)
                        # Add each file to the ZIP archive
                        zip_file.writestr(f"{i}.png", tile_data)

            # Set the appropriate headers for returning a ZIP file
            headers = {
                "Content-Type": "application/zip",
                "Content-Disposition": f"attachment; filename=tiles.zip"
            }

            # Return the ZIP file data and headers
            response = Response(content=zip_data.getvalue(), headers=headers)
            return response
        raise ImageNotFound(status_code=404, detail='Image not found')

