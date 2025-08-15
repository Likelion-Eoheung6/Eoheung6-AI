from collections import OrderedDict
import uuid
from custom_error.qdrant_info_id_not_found_error import QdrantInfoIdNotFoundError
from common.config.qdrant_config import qdrant_client, openai_client, tag_collection, detail_collection
from qdrant_client.models import PointStruct, models

class IncludeReview:
    def __init__(self, info_id, title: str, tag: str, is_full):
        print(f"info_id={info_id}, is_full={is_full}")
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.detail_collection = detail_collection
        self.info_id = info_id
        self.tag = tag
        self.title = title
        self.is_full = is_full

    def save(self):
        text = f"infoId: {self.info_id}, title: {self.title}, tag: {self.tag}, isFull: {self.is_full}"
        print(f"infoId={self.info_id}, title={self.title}, tag={self.tag}, isFull={self.is_full}")
        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        ).data[0].embedding

        self.qdrant_client.upsert(
            collection_name=self.detail_collection,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=response,
                    payload={"info_id": self.info_id,
                             "title": self.title,
                             "tag": self.tag,
                             "is_full": self.is_full
                         }
                )
            ]
        )
        return OrderedDict([
            ("infoId", self.info_id),
            ("title", self.title),
            ("tag", self.tag),
            ("isFull", self.is_full)
        ])

class WithoutReview:
    def __init__(self, info_id: int, tag: str, is_full: bool):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.tag_collection = tag_collection
        self.info_id = info_id
        self.tag = tag
        self.is_full = is_full
    
    def save(self):
        text = f"infoId: {self.info_id}, tag: {self.tag}, isFull: {self.is_full}"

        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        ).data[0].embedding

        self.qdrant_client.upsert(
        collection_name=self.tag_collection,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=response,
                payload={"info_id": self.info_id,
                         "tag": self.tag,
                         "is_full": self.is_full
                         }
                )
            ]
        )

        return OrderedDict([
            ("infoId", self.info_id),
            ("tag", self.tag),
            ("isFull", self.is_full)
        ])
    

class ChangeFlag:
    # 1. 생성자: 필요한 모든 정보를 명확하게 외부에서 주입받습니다.
    # 이렇게 하면 클래스의 재사용성과 테스트 용이성이 크게 향상됩니다.
    def __init__(self, info_id: int, is_full: bool):
        self.qdrant_client = qdrant_client
        self.info_id = info_id
        self.is_full = is_full
        self.tag_collection = tag_collection
        self.detail_collection = detail_collection
        print(f"ChangeFlag initialized for info_id: {self.info_id}, is_full: {self.is_full}")

    # 2. 실행 메소드: 모든 로직을 이 메소드 안에서 순차적으로 명확하게 처리합니다.
    def execute(self):
        print("--- Executing ChangeFlag ---")

        # 내부 헬퍼 함수: 특정 컬렉션에서 info_id로 point의 고유 id를 찾아오는 역할
        def get_point_id(collection_name: str) -> str | None:
            points, _ = self.qdrant_client.scroll(
                collection_name=collection_name,
                scroll_filter=models.Filter(must=[
                    models.FieldCondition(key="info_id", match=models.MatchValue(value=self.info_id))
                ]),
                limit=1 # ID는 하나만 필요함
            )
            if points:
                point_id = points[0].id
                print(f"Found point in '{collection_name}' with ID: {point_id}")
                return point_id
            print(f"Point not found in '{collection_name}' for info_id: {self.info_id}")
            return None

        # 2-1. 두 컬렉션에서 각각 point ID를 찾습니다.
        tag_point_id = get_point_id(self.tag_collection)
        detail_point_id = get_point_id(self.detail_collection)

        # 2-2. 두 컬렉션 모두에 해당 info_id가 없으면 에러를 발생시킵니다.
        if tag_point_id is None and detail_point_id is None:
            raise QdrantInfoIdNotFoundError(f"info_id '{self.info_id}' not found in any collection.")

        # 2-3. point ID를 찾은 경우에만 payload를 업데이트합니다. (중복 실행 방지)
        if tag_point_id:
            print(f"Updating payload for tag collection...")
            self.qdrant_client.set_payload(
                collection_name=self.tag_collection,
                payload={"is_full": self.is_full},
                points=[tag_point_id],
                wait=True
            )
        
        if detail_point_id:
            print(f"Updating payload for detail collection...")
            self.qdrant_client.set_payload(
                collection_name=self.detail_collection,
                payload={"is_full": self.is_full},
                points=[detail_point_id],
                wait=True
            )

        print("--- ChangeFlag Execution Finished Successfully ---")
        # 성공적으로 완료되었음을 알리는 간단한 결과를 반환할 수 있습니다.
        return {"status": "success", "updated_info_id": self.info_id}