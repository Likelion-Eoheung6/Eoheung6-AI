import os
from service.config.qdrant_singleton import client
from qdrant_client.models import SearchRequest, PointStruct, Filter, FieldCondition, MatchValue
from dotenv import load_dotenv
from services.tag import get_user_tags
from services.review import get_user_reviews
from services.history import get_user_class_titles
from service.template.sql_template import FilterOpenClass
from service config.db import db
from transformers import AutoTokenizer, AutoModel
from datetime import datetime
import torch

# Embedding part
load_dotenv()
MODEL_NAME = os.environ.get("DEBERTA_MODEL_NAME")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()

# Vector Search part
COLLECTION_NAME = os.environ.get("QDRANT_COLLECTION_NAME")

def vector_embed(user_id):
    # 1. 사용자 정보 수집
    tags = get_user_tags(user_id)
    reviews = get_user_reviews(user_id)
    history = get_user_class_titles(user_id)

    profile = (
        f"이 사용자는 '{', '.join(tags)}' 태그를 선호하고, "
        f"'{', '.join(history)}' 클래스를 수강했으며, "
        f"리뷰로는 '{'; '.join(reviews)}' 같은 표현을 사용했습니다."
    )

    user_vector = embed_text(profile)
    candidates = search_similar_classes(user_vector)
    open_classes = filter_open_classes([c["class_id"] for c in candidates])
    # 프롬프트 반환, call_ai 위임
    return answer


# 문장 기반 Embed 된 데이터 쿼리. 유사도 추출
def embed_text(text: str) -> list[float]:
    inputs = tokenizer(text, return_tensors="pt",
                       truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().tolist()

# 비슷한 클래스 서치
def search_similar_class(query_vector:
                         list[float], top_k: int = 5) -> list[dict]:
    search_result = client.search(
        collection_name = COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )

    return [
        {
            "class_id": point.payload.get("class_id"),
            "title": point.payload.get("title"),
            "description": point.payload.get("description"),
            "score": point.score
        }
        for point in search_result
    ]
