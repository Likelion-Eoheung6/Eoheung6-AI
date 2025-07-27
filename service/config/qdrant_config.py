from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 임베딩 모델 API key 환경변수 꺼내오기
API_KEY = os.environ.get("AI_API_KEY")
openai_client = OpenAI(api_key=API_KEY)

# Qdrant 클라이언트 (도커에서 꺼내오기)
qdrant_client = QdrantClient(host="localhost", port=6333)

# RDB Table = Collection
qdrant_collection = "test"


def init_qdrant_collection():
    if not qdrant_client.collection_exists(qdrant_collection):
        qdrant_client.recreate_collection(
            collection_name=qdrant_collection,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
