import os
import uuid

import pandas as pd
from qdrant_client.http.models import VectorParams, PointStruct, Distance

from app.config import COLLECTION_NAME, LIBRARY_IMAGES_DIR, INIT_IMAGES_FILE
from app.src.processing.models import get_models
from app.src.processing.tasks import generate_description_args
from app.src.services.qdrant import QdrantService


def init_collection(collection: str = COLLECTION_NAME):
    try:
        QdrantService().client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=1024, distance=Distance.DOT),
        )
    except:
        print("Collection already created")


def init_images(emb_model):
    images_df = pd.read_csv(INIT_IMAGES_FILE, sep="|")
    points = [PointStruct(id=row.Index, vector=emb_model.encode(row.description),
                          payload={"filename": row.filename, "filepath": os.path.join(LIBRARY_IMAGES_DIR, row.filename),
                                   "title": row.title, "author": row.author}) for row in images_df.itertuples()]

    QdrantService().add_vector(points)


def init_images_os(processor_, model_, emb_model_):
    images_df = pd.read_csv(INIT_IMAGES_FILE, sep="|")

    images = []
    for file in os.listdir(LIBRARY_IMAGES_DIR):
        filename = os.fsdecode(file)
        filepath = os.path.join(LIBRARY_IMAGES_DIR, filename)
        title = images_df[images_df['filename'] == filename]['title'].iloc[0]
        author = images_df[images_df['filename'] == filename]['author'].iloc[0]

        description = generate_description_args(filepath, processor_=processor_, model_=model_)
        print(description)

        images.append({
            "filename": filename,
            "title": title,
            "author": author,
            "description": description,
            "filepath": filepath
        })

    points = [PointStruct(id=uuid.uuid4().hex, vector=emb_model_.encode(image_metadata['description']),
                          payload={"filename": image_metadata['filename'],
                                   "filepath": image_metadata['filepath'],
                                   "title": image_metadata['title'],
                                   "author": image_metadata['author']}) for image_metadata in images]

    QdrantService(collection_name="os_description").add_vector(points)



if __name__ == '__main__':
    _, _, emb_model = get_models()
    init_images(emb_model)
