import os
import shutil

from qdrant_client.http.models import PointStruct
from PIL import Image

from datetime import datetime

from app.config import TMP_DIR, LIBRARY_IMAGES_DIR
from app.src.services.qdrant import QdrantService


def save_tmp_details(image_filepath: str) -> str:
    current_datetime = datetime.now()
    timestamp = datetime.timestamp(current_datetime)
    tmp_dir = f"{TMP_DIR}/tmp_{timestamp}"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    shutil.copy(image_filepath, tmp_dir)

    return os.path.join(tmp_dir, image_filepath)


def generate_outputs_args(image_fp, description, processor_=None, model_=None, emb_model_=None) -> list:
    tmp_filepath = save_tmp_details(image_fp)

    if not description:
        final_description = generate_description_args(image_path=tmp_filepath, processor_=processor_,
                                                      model_=model_)
        vector = emb_model_.encode(final_description).tolist()
        result = QdrantService(collection_name='os_description').search_query(vector=vector)

    else:
        final_description = description
        vector = emb_model_.encode(final_description).tolist()
        result = QdrantService(collection_name='os_description').search_query(vector=vector)

    payload = result[0].payload
    return [payload['title'], f"{result[0].score}", final_description, payload['filepath']]


def generate_description_args(image_path: str, processor_=None, model_=None) -> str:
    raw_image = Image.open(image_path).convert('RGB')

    # conditional image captioning
    text = "a work of art of"
    inputs = processor_(raw_image, text, return_tensors="pt")

    out = model_.generate(**inputs)

    # unconditional image captioning
    inputs = processor_(raw_image, return_tensors="pt")

    out = model_.generate(**inputs)
    return processor_.decode(out[0], skip_special_tokens=True)


def save_original_art_args(image, title, author, description, emb_model=None):
    image_name = image[0].split('/')[-1]
    point = [PointStruct(vector=emb_model.encode(description),
                         payload={"filename": image_name, "filepath": os.path.join(LIBRARY_IMAGES_DIR, image_name),
                                  "title": title, "author": author})]

    QdrantService().add_vector(point)
