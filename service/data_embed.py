import os
import uuid
from service.config.qdrant_config import qdrant_client, openai_client, qdrant_collection
from qdrant_client.models import PointStruct
from dotenv import load_dotenv
from openai import OpenAI

# 유저의 선호 태그를 Vector Embedding
# 유저의 고유 ID (MySQL Primary Key)로 식별

load_dotenv()


class DataEmbedding:
    def __init__(self):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.qdrant_collection = qdrant_collection

    def save(self, class_id: int, tag: str, class_name: str, review: str) -> None:

        text = f"class_id: {class_id}, tag: {tag}, class: {class_name}, review: {review}"

        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        ).data[0].embedding

        self.qdrant_client.upsert(
        collection_name=self.qdrant_collection,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=response,
                payload={"class_id": class_id,
                         "tag": tag,
                         "class": class_name,
                         "review": review
                         }
                )
            ]
        )