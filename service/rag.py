import uuid
import os
from dotenv import load_dotenv
from openai import OpenAI
from service.config.qdrant_config import qdrant_client, openai_client, qdrant_collection
from qdrant_client.models import Filter, FieldCondition, MatchValue
import numpy as np


class RagAnswer:
    def __init__(self):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.qdrant_collection = qdrant_collection
    
    def call(self, tag: str, class_name: str, review: str):
        data = self.sentence(tag, class_name, review)

        embed_query = openai_client.embeddings.create(
            input=data,
            model="text-embedding-3-small"
        ).data[0].embedding

        search_result = qdrant_client.search(
            collection_name=qdrant_collection,
            query_vector=embed_query,
            limit=1,
            query_filter=Filter(
                must_not=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=USER_ID)  # 제외할 user_id
                    )
                ]
            )
        )

        print(search_result[0].payload)
        # json 전체는 [result.payload for result in search_result]를 반환
        return search_result[0].payload
    
    def re_call(self, class_id: int, tag: str, class_name: str, review: str):
        data = self.sentence(tag, class_name, review)

        embed_query = openai_client.embeddings.create(
            input=data,
            model="text-embedding-3-small"
        ).data[0].embedding
        
        search_result = qdrant_client.search(
            collection_name=qdrant_collection,
            query_vector=embed_query,
            limit=1,
            query_filter= Filter(
                must_not=[
                    FieldCondition(
                        key="class_id",
                        match=MatchValue(value=int(class_id))
                    )
                ]
            )
        )
        
        return search_result[0]
    
    def sentence(self, tag, class_name, review):
        return f" \"tag\": {tag}, \"class_name\": {class_name}, \"review\": {review}"
    
    def weights(pref_tag, common_tag, alpha = 1.2, beta = 0.8):
        # 선호 태그에서 선호 - 클래스 공통 분모가 차지하는 비
        overlap_ratio = common_tag / pref_tag

        overlap_effect = (1 / pref_tag) ** beta

        base_tag = 0.5
        bonus = 0.5

        w_tag = base_tag + bonus * (overlap_effect * (1 + overlap_effect))
        return min(w_tag, 1.0)

    def calc_tag_ratio(has_review:bool, tag_weight:float) -> int:
        if(has_review):
            result = tag_weight * 8
        else :
            result = tag_weight * 10
        return round(tag_weight)