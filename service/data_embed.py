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
    def __init__(self, info_id: int, tag: list[str], class_name: str):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.qdrant_collection = qdrant_collection
        self.info_id = info_id
        self.tag = tag
        self.class_name = class_name

    def save(self) -> None:

        text = f"info_id: {self.info_id}, tag: {self.tag}, class: {self.class_name}"

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
                payload={"info_id": self.info_id,
                         "tag": self.tag,
                         "class": self.class_name
                         }
            )
        ]
    )

class ReviewDataEmbedding:
    def __init__(self, info_id: int, user_id: int, review: str):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.qdrant_collection = qdrant_collection
        self.info_id = info_id
        self.user_id = user_id
        self.review = review
    
    def save(self) -> None:
        text = f"info_id: {self.info_id}, user_id: {self.user_id}, review: {self.review}"

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
                payload={"info": self.info_id,
                         "user_id": self.user_id,
                         "review": self.review
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
        search, _ = self.qdrant_client.scroll(
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
        
        
        if not search:
            raise ValueError(f"info_id={self.info_id} 에 해당하는 데이터가 없습니다.")
        if search[0].payload.get("is_full") == self.is_full:
            raise ValueError(f"is_full 값이 이미 {self.is_full} 입니다.")
    
        self.qdrant_client.set_payload(
            collection_name=self.qdrant_collection,
            payload={"is_full": self.is_full},
            points=[search[0].id]
        )
        
    def get(self):
        search, _ = self.qdrant_client.scroll(
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

        if search:
            return search[0].payload
        else:
            return None

