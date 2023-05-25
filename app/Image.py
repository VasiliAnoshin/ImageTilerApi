
import os
class PanoramicImage:
    MAX_IMAGE_SIZE = 1 * 1024 * 1024 * 1024  # 1GB

    def __init__(self, file):
        self.file = file

    def valid_image(self):
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
        if self.valid_image():
            return True



    def divide_into_tiles(image_path, tile_size):
        image = PanoramicImage.open(image_path)
        width, height = image.size
        tiles = []

        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                box = (x, y, x + tile_size, y + tile_size)
                tile = image.crop(box)
                tiles.append(tile)

        return tiles
