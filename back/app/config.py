import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(ROOT_DIR, 'data/images')


class SuperUser:
    USERNAME = os.environ['SUPERUSER_USERNAME']
    PWD = os.environ['SUPERUSER_PWD']


# Secret key for JWT encoding and decoding
SECRET_KEY = os.getenv('SECRET_KEY', "")
ALGORITHM = os.getenv('ALGORITHM', "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)
