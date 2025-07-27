import uuid
import os
from dotenv import load_dotenv
from openai import OpenAI
from service.config.qdrant_config import qdrant_client, openai_client, qdrant_collection


class RagAnswer:
    def __init__(self):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.qdrant_collection = qdrant_collection
    
    def call(self, tag: str, class_name: str, review: str) -> None:
        data = f" \"tag\": {tag}, \"class_name\": {class_name}, \"review\": {review}"

        embed_query = openai_client.embeddings.create(
            input=data,
            model="text-embedding-3-small"
        ).data[0].embedding

        search_result = qdrant_client.search(
            collection_name=qdrant_collection,
            query_vector=embed_query,
            limit=1
        )
        return [result.payload for result in search_result]