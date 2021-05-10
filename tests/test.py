import datetime as dt
import unittest
from unittest import mock
import base64
import api.image_api as image_api


class Tests(unittest.TestCase):
    TEST_DATETIME = dt.datetime(2021, 1, 1)
    TEST_IMAGES_DIR = "tests/test_images/"
    TEST_IMAGE_FILES = [
        f"{TEST_IMAGES_DIR}test.jpg",
        f"{TEST_IMAGES_DIR}test_1.png",
        f"{TEST_IMAGES_DIR}test_2.jpg",
    ]

    TEST_IMAGES = [
        base64.b64encode(open(image, "rb").read()) for image in TEST_IMAGE_FILES
    ]

    TEST_IMAGE_STRINGS = [image.decode("utf-8") for image in TEST_IMAGES]

    def setUp(self):

        image_api.app.config["TESTING"] = True
        image_api.app.config["DEBUG"] = True
        self.app = image_api.app.test_client()

    def tearDown(self):
        pass

    @mock.patch("psycopg2.connect")
    @mock.patch("builtins.open")
    def test_add_image(self, mock_file, mock_connect):

        headers = {"username": "michael"}

        params = {
            "image_name": "test",
            "access": "private",
            "image_data": self.TEST_IMAGE_STRINGS[0],
        }

        response = self.app.post("/image/AddImage", headers=headers, json=params)
        mock_file.assert_called_once_with("images/michael/test.png", "wb")

        mock_file().__enter__().write.assert_called_once_with(self.TEST_IMAGES[0])

        self.assertEqual(response.json["message"], "Image Saved")
        self.assertEqual(response.status_code, 200)

    @mock.patch("psycopg2.connect")
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=TEST_IMAGES[1])
    def test_get_image(self, mock_file, mock_connect):

        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value
        mock_cur.fetchone.return_value = ("michael", "test", True, self.TEST_DATETIME)

        headers = {"username": "michael"}

        params = {
            "image_name": "test",
        }
        expected_json = {
            "username": "michael",
            "access": "private",
            "date_added": "Fri, 01 Jan 2021 00:00:00 GMT",
            "image_data": self.TEST_IMAGE_STRINGS[1],
            "image_name": "test",
        }

        response = self.app.get("/image/GetImage", headers=headers, query_string=params)

        mock_file.assert_called_once_with("images/michael/test.png", "rb")

        self.assertEqual(response.json, expected_json)

        self.assertEqual(response.status_code, 200)
