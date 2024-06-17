import os

import pandas as pd
from qdrant_client.http.models import VectorParams, PointStruct, Distance

from app.config import COLLECTION_NAME, LIBRARY_IMAGES_DIR, INIT_IMAGES_FILE
from app.src.processing.models import get_models
from app.src.services.qdrant import QdrantService


def init_collection():
    try:
        QdrantService().client.create_collection(
            collection_name=COLLECTION_NAME,
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

if __name__ == '__main__':
    _, _, emb_model = get_models()
    init_images(emb_model)