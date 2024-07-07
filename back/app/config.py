import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(ROOT_DIR, 'data/images')


class SuperUser:
    USERNAME = os.environ['SUPERUSER_USERNAME']
    PWD = os.environ['SUPERUSER_PWD']