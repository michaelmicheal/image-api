from api.constants import IMAGES_DIR
from api.images_manager import ImagesManager
from api.pg_manager import PGManager
from api.image import Image, ImageInfo


class DataManager:
    def __init__(self):
        self.im = ImagesManager(IMAGES_DIR)
        self.pgm = PGManager()

    def __enter__(self):
        self.pgm = self.pgm.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.pgm.__exit__(exc_type, exc_value, exc_traceback)

    def add_user(self, username):
        self.pgm.add_user(username)
        user_id = self.pgm.get_user_id(username)
        self.im.add_user(username)
        return user_id

    def add_image(self, image):
        user_id = self.pgm.get_user_id(image.username)
        if user_id is None:
            user_id = self.add_user(image.username)
        self.pgm.add_image(
            image_name=image.image_name,
            username=image.username,
            is_public=image.is_public,
        )
        self.im.add_image(image)

    def get_image(self, username, image_name):
        image_info = ImageInfo(*self.pgm.get_image_info(username, image_name))
        image_data = self.im.get_image(image_info)
        return Image.from_info(image_info, image_data)

    def find_images(self, name_search, username=None, is_public=None):
        image_infos = [
            ImageInfo(*info)
            for info in self.pgm.find_images(name_search, username, is_public)
        ]
        images = [
            Image.from_info(info, self.im.get_image(info)) for info in image_infos
        ]

        return images
