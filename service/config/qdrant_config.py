import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from dotenv import load_dotenv
from openai import OpenAI

from custom_error.openai_api_key_not_found_error import OpenAIApiKeyNotFoundError
from custom_error.qdrant_connection_failed_error import QdrantConnectionFailedError

load_dotenv()

# 임베딩 모델 API key 환경변수 꺼내오기
API_KEY = os.environ.get("AI_API_KEY")
if API_KEY is None:
    raise OpenAIApiKeyNotFoundError()

openai_client = OpenAI(api_key=API_KEY)

# Qdrant 클라이언트 (도커에서 꺼내오기)
qdrant_client = QdrantClient(host="localhost", port=6333)

# RDB Table = Collection
tag_collection = "tag"
review_collection = "review"


def init_qdrant_collection():
    
    if not qdrant_client.collection_exists(tag_collection):
        qdrant_client.recreate_collection(
            collection_name=tag_collection,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
    if not qdrant_client.collection_exists(review_collection):
        qdrant_client.recreate_collection(
            collection_name=review_collection,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )

    try:
        qdrant_client.collection_exists(tag_collection)
        qdrant_client.collection_exists(review_collection)
    except httpx.ConnectError:
        raise QdrantConnectionFailedError()


