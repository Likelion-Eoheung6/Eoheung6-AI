import uuid
import os
from dotenv import load_dotenv
from openai import OpenAI
from service.config.qdrant_config import qdrant_client, openai_client, review_collection, tag_collection
from qdrant_client.models import Filter, FieldCondition, MatchValue
import numpy as np
from service.config.sql_alchemy import db
from service.model.class_model import ClassHistory, ClassOpen, Review


class RagAnswer:
    def __init__(self, user_id: int, tag: str, title: str, review: str):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.review_collection = review_collection
        self.tag_collection = tag_collection
        self.user_id = user_id
        self.tag = tag
        self.title = title
        self.review = review
    
    def call(self):
        # 완성해야 함

        # 1. 수강 이력이 없음 -> tag 10개
        # FIXME USER_ID -> 추후 토큰같은 user_id 파싱
        if db.session.query(ClassHistory).filter(ClassHistory.user_id == self.user_id).first() is None:
            # text = f"info_id: {self.info_id}, tag: {self.tag}, is_full: {self.is_full}"
            data = f"tag: {self.tag}"
            
            response = self.openai_client.embeddings.create(
                input=data,
                model="text-embedding-3-small"
            ).data[0].embedding

            search= self.qdrant_client.search(
                collection_name=self.tag_collection,
                query_vector=response,
                limit = 10,
                query_filter= Filter(
                    must_not = [
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=int(self.user_id)) # FIXME USER_ID -> user_id
                        ),
                        FieldCondition(
                            key="is_full",
                            match=MatchValue(value=True)
                        )
                    ]
                )
            )
        # 2. 수강 이력은 있고, 리뷰는 없음
        elif db.session.query(Review).filter(Review.user_id == self.user_id).first() is None:
            data = f"tag: {self.tag}, title: {self.title}"

            response = self.openai_client.embeddings.create(
                input=data,
                model="text-embedding-3-small"
            ).data[0].embedding

            search, _ = self.qdrant_client.search(
                collection_name=self.review_collection, # FIXME collection 분리로 인해 수정 필요
                query_vector=response,
                limit = 10,  # FIXME for문 변경 시 수정 필요
                query_filter= Filter(
                    must_not = [
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=int(self.user_id)) # FIXME USER_ID -> user_id
                        ),
                        FieldCondition(
                            key="is_full",
                            match=MatchValue(value=True)
                        )
                    ]
                )
            )

        else:
            data = f"tag: {self.tag}, title: {self.title}, review: {self.review}"

            response = self.openai_client.embeddings.create(
                input=data,
                model="text-embedding-3-small"
            ).data[0].embedding

            search, _ = self.qdrant_client.search(
                collection_name=self.review_collection, # FIXME collection 분리로 인해 수정 필요
                query_vector=response,
                limit = 10,
                query_filter= Filter(
                    must_not = [
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=int(self.user_id)) # FIXME USER_ID -> user_id
                        ),
                        FieldCondition(
                            key="is_full",
                            match=MatchValue(value=True)
                        )
                    ]
                )
            )
        # print(search[0].payload)

        if(search):
            return search # record 형태임. 꺼낼 때 search[0].payload.get("info_id")로 꺼낼 수 있을듯?
        else:
            raise ValueError("현재 진행 중인 클래스가 없습니다.")
