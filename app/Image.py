
import os
from PIL import Image
import logging 

logger = logging.getLogger(__name__)

class PanoramicImage:
    MAX_IMAGE_SIZE = 1 * 1024 * 1024 * 1024  # 1GB

    def __init__(self, file, image_id:str, user_id:int):
        self.file = file
        self.image_id = image_id
        self.user_id = user_id

    def _validate_image(self):
        if self.file.content_type.startswith("image/"):
            try:
                if self.file.size > PanoramicImage.MAX_IMAGE_SIZE:
                    raise Exception(status_code=400, detail="Image size exceeds the limit of 1GB.")
                return True
            except Exception:
                raise Exception(status_code=400, detail="Unable to determine image size.")
        else:
            raise Exception(status_code=400, detail="Invalid file format. Only images are allowed.")

    def upload_image(self):
        logger.info('Image validator ... ')
        if self._validate_image():
            logger.info('Open image ... ')
            image = Image.open(self.file.file)
            logger.info('Divide into tiles ... ')
            tiles = self._divide_into_tiles(image, tile_size=(256, 256))
            logger.info('Save original image ... ')
            self.save_original_image()
            logger.info('Save tiles ... ')
            # self.save_tiles(tiles)

    def save_original_image(self):
        try:
            logger.info('Save the panoramic image')
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
            logger.debug('File was saved successfully ...')
        except Exception as ex:
            raise ex

    def save_tiles(self, tiles):
        # Generate a unique image ID
        image_id = str(len(image_tiles) + 1)

        # Create a directory to store the tiles
        directory = os.path.join('tiles', image_id)
        os.makedirs(directory)

        # Save each tile as an individual image file
        for i, tile in enumerate(tiles):
            tile_path = os.path.join(directory, f'{i}.png')
            tile.save(tile_path)

        # Associate the image ID with the tiles
        image_tiles[image_id] = tiles

    def _divide_into_tiles(self, image, tile_size):
        width, height = image.size
        tiles = []

        for y in range(0, height, tile_size[0]):
            for x in range(0, width, tile_size[1]):
                box = (x, y, x + tile_size[1], y + tile_size[0])
                tile = image.crop(box)
                tiles.append(tile)

        return tiles
