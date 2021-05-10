from dotenv import load_dotenv
import os
from enum import Enum

# Environment Variables
load_dotenv()
HOST = os.environ["HOST"]
DATABASE = os.environ["DATABASE"]
USER = os.environ["POST_USER"]
PASSWORD = os.environ["PASSWORD"]

IMAGES_DIR = "images"
