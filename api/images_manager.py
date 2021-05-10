import os


class UserExistsError(Exception):
    pass


class ImagesManager:
    def __init__(self, dir):
        self.dir = dir

    def get_image_path(self, username, image_name):
        return "/".join((self.dir, username, image_name)) + ".png"

    def add_user(self, username):
        try:
            os.mkdir("/".join((self.dir, username)))
        except FileExistsError:
            pass
        except Exception as e:
            raise e

    def add_image(self, image):
        with open(
            self.get_image_path(image.username, image.image_name), "wb"
        ) as image_file:
            image_file.write(image.image_data)

    def get_image(self, image_info):
        with open(
            self.get_image_path(image_info.username, image_info.image_name), "rb"
        ) as image_file:
            return image_file.read()
