class ImageInfo:
    def __init__(self, username, image_name, is_public, date_added):
        self.username = username
        self.image_name = image_name
        self.is_public = is_public
        self.date_added = date_added


class Image(ImageInfo):
    def __init__(self, username, image_name, is_public, image_data, date_added=None):
        ImageInfo.__init__(self, username, image_name, is_public, date_added)
        self.image_data = image_data

    @classmethod
    def from_info(cls, image_info, image_data):
        return cls(
            image_info.username,
            image_info.image_name,
            image_info.is_public,
            image_data,
            image_info.date_added,
        )

    @classmethod
    def from_request(cls, username, dict):
        image_name = dict["image_name"]
        access = dict["access"]

        if access in ["private", "public"]:
            is_public = access == "public"
        else:
            raise Exception

        image_data = dict["image_data"].encode("utf-8")

        return cls(username, image_name, is_public, image_data)

    def to_response(self):

        access = "private" if self.is_public else "private"

        return {
            "image_name": self.image_name,
            "username": self.username,
            "access": access,
            "date_added": self.date_added,
            "image_data": self.image_data.decode("utf-8"),
        }
