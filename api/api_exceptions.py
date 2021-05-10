from flask import jsonify


class APIException(Exception):
    def __init__(self, message, status_code):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_response(self):
        return jsonify({"message": self.message})


class DatabaseAuthenticationError(APIException):
    def __init__(self):
        APIException.__init__(self, "Database authentication error", 511)


class UserDoesNotExistError(APIException):
    def __init__(self):
        APIException.__init__(
            self,
            "There is not an existing user with that username",
            511,
        )


class ImageDoesNotExistError(APIException):
    def __init__(self):
        APIException.__init__(
            self,
            "There is not an image associated with the image_name and username",
            511,
        )


class ImageAlreadyExistsError(APIException):
    def __init__(self):

        APIException.__init__(
            self, "An image with image_name and username already exists", 511
        )
