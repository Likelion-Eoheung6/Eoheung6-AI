from service.config.qdrant_singleton import QdrantClient

client = QdrantClient(host="localhost", port=6333)

def callAI():
    # deBERTa가 벡터 임베딩
    # Qdrant에서 Vector Search
        # id를 MySQL에 재검색
        # 기간 만료 클래스일시
        # 재검색
    # context로 정리
    # prompt 생성
    # 답변 반환
    return