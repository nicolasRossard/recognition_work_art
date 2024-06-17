import os

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

from app.config import COLLECTION_NAME


class QdrantService:
    # todo manage error conn
    def __init__(self, collection_name: str = COLLECTION_NAME, host: str = os.environ['QDRANT_HOST'], port: int = int(os.environ['QDRANT_PORT'])):
        self.client = QdrantClient(host, port=port)
        self.collection_name = collection_name

    def search_query(self, vector):
        search_result = self.client.search(
            collection_name=self.collection_name, query_vector=vector, limit=1)
        return search_result

    def add_vector(self, points: list[PointStruct], collection_name=None):

        if collection_name is None:
            collection_name = self.collection_name

        self.client.upsert(
            collection_name=collection_name,
            wait=True,
            points=points,
        )