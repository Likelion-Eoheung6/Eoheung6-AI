import uuid
import os
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


# 유저의 선호 태그를 Vector Embedding
# 유저의 고유 ID (MySQL Primary Key)로 식별

load_dotenv()

# 임베딩 모델 API key 환경변수 꺼내오기
API_KEY = os.environ.get("AI_API_KEY")
client = OpenAI(api_key=API_KEY)

# Qdrant 클라이언트 (도커에서 꺼내오기)
q_client = QdrantClient(host="localhost", port=6333)

# RDB Table = Collection
qdrant_collection = "test"

# ddl-auto = create로 선언
q_client.recreate_collection(
    collection_name=qdrant_collection,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)  # size는 벡터 차원
)

def embedding_user_data():
    return 0