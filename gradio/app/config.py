import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(ROOT_DIR, 'models')
TMP_DIR = os.path.join(ROOT_DIR, 'tmp')

LIBRARY_IMAGES_DIR = os.path.join(ROOT_DIR, 'data/images')
INIT_IMAGES_FILE = os.path.join(ROOT_DIR, 'data/init/init_images.csv')

COLLECTION_NAME = "original_art_description"