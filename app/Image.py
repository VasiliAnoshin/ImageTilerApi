
import os
from PIL import Image
import logging 
from fastapi import UploadFile

logger = logging.getLogger(__name__)

class ImageValidationException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class PanoramicImage:
    MAX_IMAGE_SIZE = 1 * 1024 * 1024 * 1024  # 1GB

    def __init__(self, file:UploadFile, image_id:str, user_id:int, tile_sizes:list)->None:
        """ 
        Initializes an instance of the class.
        Args:
            file: The file object representing the image file.
            image_id (str): The unique identifier for the image.
            user_id (int): The identifier for the user associated with the image.
            tile_sizes (list): A list of tile sizes for the image.

        """
        self.file = file
        self.image_id = image_id
        self.user_id = user_id
        self.tile_sizes = tile_sizes
        self.size_to_img_col = {}

    def _validate_image(self)->bool:
        """
        Validates the image file.

        Raises:
            ImageValidationException: If the file format is invalid or the image size exceeds the limit.

        Returns:
            bool: True if the image is valid.

        """
        if self.file is None:
            raise ImageValidationException(status_code=400, detail='No file found')
        
        if not self.file.content_type.startswith("image/"):
            raise ImageValidationException(status_code=400, detail="Invalid file format. Only images are allowed.")

        try:
            if self.file.size > PanoramicImage.MAX_IMAGE_SIZE:
                raise ImageValidationException(status_code=400, detail="Image size exceeds the limit of 1GB.")
        except Exception:
            raise ImageValidationException(status_code=400, detail="Unable to determine image size.")

        return True

    def upload_image_handler(self) -> None:
        """
        Handles the upload of an image.

        This method performs the following steps:
        1. Validates the image file.
        2. Opens the image.
        3. Divides the image into tiles based on the specified tile sizes.
        4. Saves the original image.
        5. Saves the tiles.

        Returns:
            None

        """
        logger.info('Image validator ... ')
        if self._validate_image():
            logger.info('Open image ... ')
            image = Image.open(self.file.file)
            logger.info('Divide into tiles ... ')
            for tile_sizes in self.tile_sizes:
                name = f"{tile_sizes[0]}x{tile_sizes[1]}" 
                self.size_to_img_col[name] = self._divide_into_tiles(image, tile_size=tile_sizes)
            logger.info('Save original image ... ')
            self.save_original_image()
            logger.info('Save tiles ... ')
            self.save_tiles()

    def save_original_image(self)->None:
        """Save the panoramic origin image 
        
        Raises:
            Exception: If an error occurs while saving the file.
        
        Returns:
            None
        """
        try:
            user_dir = os.path.join(os.getcwd(), "app", "Data", f"{self.user_id}")
            image_dir = os.path.join(user_dir, self.image_id)
            origin_pic =  os.path.join(image_dir, self.file.filename)
            logger.debug('Check that dirtectory with the same user is exist.')
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            logger.debug('Create new user image directory')
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            logger.debug('save origin file ...')
            self.file.file.seek(0)
            with open(origin_pic, "wb") as f:
                f.write(self.file.file.read())
            logger.info('File was saved successfully ...')
        except Exception as ex:
            raise ex

    def save_tiles(self) -> None:
        """
        Saves the tiles of the image to individual image files.

        The method performs the following steps:
        1. Creates a directory to store the tiles.
        2. Saves each tile as an individual image file within the directory.

        Returns:
            None

        """
        cur_dir = os.path.join(os.getcwd(), "app", "Data", f"{self.user_id}", self.image_id)
        for tile_size in self.size_to_img_col:
            logger.info('Create a directory to store the tiles')
            directory = os.path.join(cur_dir, f'{tile_size} tiles')
            if not os.path.exists(directory):
                os.makedirs(directory)

            logger.info('Save each tile as an individual image file')
            for i, tile in enumerate(self.size_to_img_col[tile_size]):
                tile_path = os.path.join(directory, f'{i}.png')
                tile.save(tile_path)
                logger.debug(f't{i} was saved successfully ...')
            logger.info(f'{tile_size} save successfully')
        logger.info('All Tiles was saved.')

       

    def _divide_into_tiles(self, image:Image, tile_size:tuple)->list:
        """
        Divides an image into tiles of the specified size.

        Args:
            image: The image to be divided into tiles.
            tile_size (tuple): The size of each tile in the format (height, width).

        Returns:
            list: A list of image tiles.

        """
        if image is None:
            raise ValueError('provided image for tiles divide is None')
        if type(tile_size) is not tuple:
            raise ValueError(f'provided tile size expected to be tuple like (256,256) recieved as {tile_size}')
        
        width, height = image.size
        tiles = []

        for y in range(0, height, tile_size[0]):
            for x in range(0, width, tile_size[1]):
                box = (x, y, x + tile_size[1], y + tile_size[0])
                tile = image.crop(box)
                tiles.append(tile)

        return tiles
