import os
import uuid
from custom_error.qdrant_info_id_not_found_error import QdrantInfoIdNotFoundError
from common.config.qdrant_config import qdrant_client, openai_client, tag_collection, detail_collection
from qdrant_client.models import PointStruct, models
from dotenv import load_dotenv
from openai import OpenAI

# 유저의 선호 태그를 Vector Embedding
# 유저의 고유 ID (MySQL Primary Key)로 식별

load_dotenv()


class IncludeReview:
    def __init__(self, info_id: int, title: str, tag: list[str], user_id:int, review:str, is_full: bool):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.detail_collection = detail_collection
        self.info_id = info_id
        self.tag = tag
        self.title = title
        self.user_id = user_id
        self.is_full = is_full

    def save(self):

        # text = f"info_id: {self.info_id}, title: {self.title}, tag: {self.tag}, user_id: {self.user_id}, review: {self.review}, is_full {self.is_full}"
        text = f"info_id: {self.info_id}, title: {self.title}, tag: {self.tag}, user_id: {self.user_id}, is_full {self.is_full}"

        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        ).data[0].embedding

        self.qdrant_client.upsert(
            collection_name=self.detail_collection,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=response,
                    payload={"info_id": self.info_id,
                             "title": self.title,
                             "tag": self.tag,
                             "is_full": self.is_full
                         }
                )
            ]
        )
        return text

class WithoutReview:
    def __init__(self, info_id: int, tag: list[str], is_full: bool):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.tag_collection = tag_collection
        self.info_id = info_id
        self.tag = tag
        self.is_full = is_full
    
    def save(self):
        text = f"info_id: {self.info_id}, tag: {self.tag}, is_full: {self.is_full}"

        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        ).data[0].embedding

        self.qdrant_client.upsert(
        collection_name=self.tag_collection,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=response,
                payload={"info_id": self.info_id,
                         "tag": self.tag,
                         "is_full": self.is_full
                         }
                )
            ]
        )

        return text
    

class ChangeFlag:
    def __init__(self, info_id:int, is_full: bool):
        self.qdrant_client = qdrant_client
        self.tag_collection = tag_collection
        self.detail_collection = detail_collection
        self.info_id = info_id
        self.is_full = is_full

    def change(self) -> None:
        search_without_review, _ = self.qdrant_client.scroll(
            collection_name=self.tag_collection,
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

        search_include_review, _ = self.qdrant_client.scroll(
            collection_name=self.detail_collection, # FIXME IncludeReview Collection
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
        
        
        if not search_without_review and not search_include_review:
            raise QdrantInfoIdNotFoundError
        
        search1 = search_without_review[0].payload.get("is_full") if search_without_review else None
        search2 = search_include_review[0].payload.get("is_full") if search_include_review else None
        if search_without_review:
            self.qdrant_client.set_payload(
                collection_name=self.tag_collection,
                payload={"is_full": self.is_full},
                points=[search_without_review[0].id]
            )
        if search_include_review:
            self.qdrant_client.set_payload(
                collection_name=self.detail_collection,
                payload={"is_full": self.is_full},
                points=[search_include_review[0].id]
            )
        
    def get_without_review(self):
        search, _ = self.qdrant_client.scroll(
            collection_name=self.tag_collection,  # FIXME WithoutReview
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
        
    def get_include_review(self):
        search, _ = self.qdrant_client.scroll(
            collection_name=self.detail_collection,  # FIXME IncludeReview
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

