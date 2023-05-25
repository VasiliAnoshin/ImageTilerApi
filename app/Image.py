
import os
from PIL import Image
import logging 

logger = logging.getLogger(__name__)

class PanoramicImage:
    MAX_IMAGE_SIZE = 1 * 1024 * 1024 * 1024  # 1GB

    def __init__(self, file, image_id:str, user_id:int, tile_sizes:list):
        self.file = file
        self.image_id = image_id
        self.user_id = user_id
        self.tile_sizes = tile_sizes
        self.size_to_img_col = {}

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

    def upload_image_handler(self):
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

    def save_original_image(self):
        """Save the panoramic origin image """
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

    def save_tiles(self):
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

       

    def _divide_into_tiles(self, image, tile_size):
        width, height = image.size
        tiles = []

        for y in range(0, height, tile_size[0]):
            for x in range(0, width, tile_size[1]):
                box = (x, y, x + tile_size[1], y + tile_size[0])
                tile = image.crop(box)
                tiles.append(tile)

        return tiles
