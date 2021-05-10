import flask
import numpy as np
from flask import request, jsonify, Response
from api.data_manager import DataManager
from api.api_exceptions import APIException
from api.image import Image


app = flask.Flask(__name__)

# app.config["TESTING"] = testing
# app.config["DEBUG"] = debug


@app.errorhandler(APIException)
def handle_exception(e):
    response = e.to_response()
    response.status_code = e.status_code
    return response


@app.route("/image/GetImage", methods=["GET"])
def get_image():

    try:
        username = request.headers.get("username")
        image_name = request.args.get("image_name")

        with DataManager() as dm:
            image = dm.get_image(username, image_name)

        return jsonify(image.to_response())

    except APIException as e:
        raise e
    except Exception as e:
        raise e
        raise APIException("Internal Server Error", 500)


@app.route("/image/FindImages", methods=["GET"])
def find_images():

    try:
        username = request.headers.get("username")
        params = request.args
        name_search = params.get("name_search")
        access = params.get("access")
        if access in ["private", "public"]:
            is_public = access == "public"
        elif access is None:
            is_public = None
        else:
            raise APIException("access must be one of ['private', 'pubic']", 400)

        with DataManager() as dm:
            images = dm.find_images(name_search, username, is_public)

        results = [image.to_response() for image in images]

        return jsonify(results)

    except APIException as e:
        raise e
    except Exception as e:
        raise APIException("Internal Server Error", 500)


@app.route("/image/AddImage", methods=["POST"])
def add_image():
    try:

        username = request.headers.get("username")

        image = Image.from_request(username, request.json)
        with DataManager() as dm:
            dm.add_image(image)
        response = {"message": "Image Saved"}

        return jsonify(response)
    except APIException as e:
        raise e
    except Exception as e:
        raise e
        raise APIException("Internal Server Error", 500)


@app.route("/image/AddImagesBulk", methods=["POST"])
def add_images():
    try:
        username = request.headers.get("username")

        data = request.json

        image_list = [Image.from_request(username, image_dict) for image_dict in data]

        with DataManager() as dm:
            for image in image_list:
                dm.add_image(image)

        return jsonify({"message": "Images Saved"})

        return Response(response=response, status=200, mimetype="application/json")
    except APIException as e:
        raise e
    except Exception as e:
        raise e
        raise APIException("Internal Server Error", 500)


if __name__ == "__main__":
    app.run()
