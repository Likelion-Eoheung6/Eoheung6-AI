from service.config.qdrant_singleton import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os

def init_qdrant_collection(client: QdrantClient, collection_name: str = "class_vectors", dim: int = 768):
    if not client.collection_exists(collection_name):
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )
