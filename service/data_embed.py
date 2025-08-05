import os
import uuid
from service.config.qdrant_config import qdrant_client, openai_client, qdrant_collection
from qdrant_client.models import PointStruct, models
from dotenv import load_dotenv
from openai import OpenAI

# 유저의 선호 태그를 Vector Embedding
# 유저의 고유 ID (MySQL Primary Key)로 식별

load_dotenv()


class TagAndClassDataEmbedding:
    def __init__(self):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.qdrant_collection = qdrant_collection

    def save(self, class_id: int, tag: str, class_name: str) -> None:

        text = f"class_id: {class_id}, tag: {tag}, class: {class_name}"

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
                         "class": class_name
                        #  "review": review
                         }
                )
            ]
        )

class ReviewDataEmbedding:
    def __init__(self):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.qdrant_collection = qdrant_collection
    
    def save(self, class_id: int, user_id: int, review: str) -> None:
        text = f"class_id: {class_id}, user_id: {user_id}, review: {review}"

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
                         "user_id": user_id,
                         "review": review
                         }
                )
            ]
        )
    

class ChangeFlag:
    def __init__(self, info_id:int, is_full: bool):
        self.qdrant_client = qdrant_client
        self.qdrant_collection = qdrant_collection
        self.info_id = info_id
        self.is_full = is_full

    def change(self) -> None:
        search = self.qdrant_client.scroll(
            collection_name=self.qdrant_collection,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="info_id",
                        match=models.MatchValue(value=self.info_id)
                    )
                ]
            ),
            limit=1
        )
        
        if search[0]:
            qdrant_client.set_payload(
                collection_name=self.qdrant_collection,
                payload={"is_full": self.is_full},
                points=search[0]
            )
        
    def get(self):
        return self.qdrant_client.scroll(
            collection_name=self.qdrant_collection,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="info_id",
                        match=models.MatchValue(value=self.info_id)
                    )
                ]
            ),
            limit=1
        )[0]

