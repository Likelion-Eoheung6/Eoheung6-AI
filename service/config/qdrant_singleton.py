from qdrant_client import QdrantClient

# 싱글톤 객체로 관리
client = QdrantClient(host="localhost", port=6333)

# 필요 시 export
__all__ = ["client"]
