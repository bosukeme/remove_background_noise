import os
import sys
import logging
import cloudinary
from cloudinary.uploader import upload

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.getcwd()
FOLDER_PATH = BASE_DIR + "/output"


class Base:

    @classmethod
    def logger_func(cls):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(filename)-25s] [%(levelname)-8s] %(message)s"
        )
        sh.setFormatter(formatter)
        sh.setLevel(logging.getLevelName("DEBUG"))
        logger.addHandler(sh)
        logger.propagate = False
        return logger


class CloudinaryUpload:
    def __init__(self):
        self.cloud_name = os.getenv('CLOUD_NAME')
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")

        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret
            )

    def upload_file(self, file_path, file_name, folder):
        result = upload(file_path, resource_type='auto', public_id=file_name, folder=folder)
        return result['secure_url']


cloudinary_upload = CloudinaryUpload()
