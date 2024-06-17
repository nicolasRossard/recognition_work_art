import os
import shutil

from qdrant_client.http.models import PointStruct

from datetime import datetime

from app.config import TMP_DIR, LIBRARY_IMAGES_DIR
from app.src.services.qdrant import QdrantService


def generate_outputs_args(image_fp, description, processor_=None, model_=None, emb_model_=None) -> list:
    current_datetime = datetime.now()
    timestamp = datetime.timestamp(current_datetime)
    tmp_dir = f"{TMP_DIR}/tmp_{timestamp}"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    shutil.copy(image_fp, tmp_dir)

    if not description:
        final_description = generate_description(image_path=os.path.join(tmp_dir, image_fp), processor=processor_,
                                                 model=model_)
    else:
        final_description = description

    vector = emb_model_.encode(final_description).tolist()

    result = QdrantService().search_query(vector=vector)

    payload = result[0].payload
    return [payload['title'], f"{result[0].score}", final_description, payload['filepath']]


def generate_description(image_path: str, processor, model) -> str:
    # TODO to implement
    pass


def save_original_art_args(image, title, author, description, emb_model=None):
    image_name = image[0].split('/')[-1]
    point = [PointStruct(vector=emb_model.encode(description),
                          payload={"filename": image_name, "filepath": os.path.join(LIBRARY_IMAGES_DIR, image_name),
                                   "title": title, "author": author})]

    QdrantService().add_vector(point)
