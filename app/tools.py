import uuid
import logging
logger = logging.getLogger(__name__)

class Tools:
    def __init__(self):
        ...
    
    @staticmethod
    def genrate_image_id(user_id:int):
        logger.info('Generate image id that will be used as identificator for image.')
        return str(f'{user_id}_{uuid.uuid4()}')