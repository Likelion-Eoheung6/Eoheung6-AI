from services.tag import get_user_tags
from services.review import get_user_reviews
from services.history import get_user_class_titles
from transformers import AutoTokenizer, AutoModel


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

def embed_text(text: str) -> list[float]:
