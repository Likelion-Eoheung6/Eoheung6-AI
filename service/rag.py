import uuid
import os
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

API_KEY = os.environ.get("AI_API_KEY")

client = OpenAI(api_key=API_KEY)
q_client = QdrantClient(host="localhost", port=6333)

qdrant_collection = "test"

q_client.recreate_collection(
    collection_name=qdrant_collection,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)  # size는 벡터 차원
)

# response.data[0].embedding

tags = "요리"
history = "할머니와 함께하는 김장하기"
reviews = "정말 재미있었습니다."

mock =(
        f"이 사용자는 '{', '.join(tags)}' 태그를 선호하고, "
        f"'{', '.join(history)}' 클래스를 수강했으며, "
        f"리뷰로는 '{'; '.join(reviews)}' 같은 표현을 사용했습니다."
    )

text = "임베딩 텍스트입니다."


response = client.embeddings.create(
    input="tag: 베이킹, class: 과자 만들기, review: 과자는 맛있어요.",
    model="text-embedding-3-small"
)

q_client.upsert(
    collection_name=qdrant_collection,
    points=[
        PointStruct(
            id=str(uuid.uuid4()),
            vector=response.data[0].embedding,
            payload={"tag": "베이킹",
                     "class": "초코 쿠키 만들기",
                     "review": "과자는 맛있어요"}
        )
    ]
)

response = client.embeddings.create(
    input="tag: 요리, class: 반찬 쉽게 만들기, review: 재미있었어요.",
    model="text-embedding-3-small"
)

q_client.upsert(
    collection_name=qdrant_collection,
    points=[
        PointStruct(
            id=str(uuid.uuid4()),
            vector=response.data[0].embedding,
            payload={"tag": "요리",
                     "class": "반찬 쉽게 만들기",
                     "review": "재미있었어요"}
        )
    ]
)

response = client.embeddings.create(
    input="tag: 운동, class: 맨몸 운동, review: 득근했어요.",
    model="text-embedding-3-small"
)

q_client.upsert(
    collection_name=qdrant_collection,
    points=[
        PointStruct(
            id=str(uuid.uuid4()),
            vector=response.data[0].embedding,
            payload={"tag": "운동",
                     "class": "맨몸 운동",
                     "review": "득근했어요"}
        )
    ]
)

query = (
    f"tag: 요리, class: 김장 담그기, review: 맛있게 먹었어요"
)

query_embedding = client.embeddings.create(
    input=query,
    model="text-embedding-3-small"
).data[0].embedding

search_result = q_client.search(
    collection_name=qdrant_collection,
    query_vector=query_embedding,
    limit=1
)

for i, result in enumerate(search_result, 1):
    print(f"[{i}] 점수: {result.score:.4f}")
    print(" payload:", result.payload)