import uuid
import os
from dotenv import load_dotenv
from openai import OpenAI
from service.config.qdrant_config import qdrant_client, openai_client, qdrant_collection
from qdrant_client.models import Filter, FieldCondition, MatchValue
import numpy as np

from service.model.class_model import ClassOpen


class RagAnswer:
    def __init__(self):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.qdrant_collection = qdrant_collection
    
    def call(self, tag: str, class_name: str, review: str):
        # 완성해야 함

        # 1. 수강 이력이 없음 -> tag 10개
        # FIXME USER_ID -> 추후 토큰같은 user_id 파싱
        if db.session.query(ClassHistory).filter(ClassHistory.user_id == USER_ID).first() is None:
            data = None # FIXME 태그 쿼리 데이터로 변경

            # tag 배열 count, for문으로 tag 개수 비례해서 10개 카운트
            # 나누어 떨어질 때, 안 떨어질 때 분기
            search, _= self.qdrant_client.search(
                collection_name=self.qdrant_collection, # FIXME collection 분리로 인해 수정 필요
                query_vector=data,
                limit = 10,  # FIXME for문 변경 시 수정 필요
                query_filter= Filter(
                    must_not = [
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=int(USER_ID)) # FIXME USER_ID -> user_id
                        )
                    ]
                )
            )
        # 2. 수강 이력은 있고, 리뷰는 없음
        elif db.session.query(Review).filter(Review.user_id == USER_ID).first() is None:
            data = None # FIXME 이후 최근 수강 이력 기반으로 변경

            search, _ = self.qdrant_client.search(
                collection_name=self.qdrant_collection, # FIXME collection 분리로 인해 수정 필요
                query_vector=data,
                limit = 10,  # FIXME for문 변경 시 수정 필요
                query_filter= Filter(
                    must_not = [
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=int(USER_ID)) # FIXME USER_ID -> user_id
                        )
                    ]
                )
            )
        # 3. 리뷰까지 있음 -> 리뷰 기반 2개, tag_weight 기반 쿼리 8개
        else:
            data = None # FIXME 이후 리뷰 포함 쿼리로 변경
            search, _ = self.qdrant_client.search(
                collection_name=self.qdrant_collection, # FIXME collection 분리로 인해 수정 필요
                query_vector=data,
                limit = 10,
                query_filter= Filter(
                    must_not = [
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=int(USER_ID)) # FIXME USER_ID -> user_id
                        )
                    ]
                )
            )
        return search # record 형태임. 꺼낼 때 search[0].payload.get("info_id")로 꺼낼 수 있을듯?
