from custom_error.user_not_found_error import UserNotFoundError
from common.config.qdrant_config import qdrant_client, openai_client, detail_collection, tag_collection
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny, models
import numpy as np
from common.config.sql_alchemy import db
from service.model.class_model import ClassApplication, ClassHistory, ClassInfo, ClassOpen, Payment, PreferTag, Review, Tag, User, EasyTag, PreferEasyTag


class RagAnswer:
    def __init__(self, user_id: int):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.detail_collection = detail_collection
        self.tag_collection = tag_collection
        self.user_id = user_id
    
    def call(self):
        user = db.session.query(User).filter(User.user_id == self.user_id).first()
        if user:
            self.user_id = user.user_id
            # 현재 오픈 중인 클래스 중에서, user_id가
            # 로그인 된 user_id와 같을 경우
            # 제외하는 로직 성공
            # self.user_id = 2
        else:
            raise UserNotFoundError()

        # 이전에 수강했던 클래스가 없는 경우
        if db.session.query(ClassApplication) \
            .join(Payment) \
            .filter(ClassApplication.user_id == self.user_id) \
            .filter(ClassApplication.payment.any(status = 'PAID')) \
                .first() is None:
            print("이전에 수강했던 클래스가 없는 경우로 진입")
            # 본인이 개설한 클래스는 제외하는 user_id 쿼리
            exclude_record = db.session.query(ClassOpen).join(ClassInfo).filter(ClassInfo.user_id == self.user_id).all()
            # print(f"exclude_record={exclude_record}")
            exclude_id = [item.id for item in exclude_record]
            # print(f"exclude_id={exclude_id}")
            
            # print(f"user_id={self.user_id}")

            normal_tag = db.session.query(PreferTag).join(Tag).filter(PreferTag.user_id == self.user_id).all()
            easy_tag = db.session.query(PreferEasyTag).join(EasyTag).filter(PreferEasyTag.user_id == self.user_id).all()
            
            whole_tag = normal_tag + easy_tag

            prefer_tag = [tags.tag.genre for tags in whole_tag]
            print(f"prefer_tag={prefer_tag}")

            data = f"tag: {prefer_tag}"
            # ---------- 막힘 ----------
            response = self.openai_client.embeddings.create(
                input=data,
                model="text-embedding-3-small"
            ).data[0].embedding

            
            search= self.qdrant_client.search(
                collection_name=self.tag_collection,
                query_vector=response,
                limit = 6,
                query_filter= Filter(
                    must_not = [
                        FieldCondition(
                            key="info_id",
                            match=MatchAny(any=exclude_id)
                        ),
                        FieldCondition(
                            key="is_full",
                            match=MatchValue(value=True)
                        )
                    ]
                )
            )
            try:
                search = [search]
            except Exception as e:
                print(f"batch 변환 실패 {str(e)}")
        # 2. 수강 이력 있음
        else:
            print("이전에 수강했던 클래스가 있는 경우로 진입")
            history = db.session.query(ClassApplication)\
                .join(ClassOpen) \
                .join(Payment) \
                .filter(ClassApplication.user_id == self.user_id)\
                .filter(ClassApplication.payment.any(status = 'PAID')) \
                .order_by(ClassOpen.open_at.desc()) \
                    .limit(3).all()
            
            exclude_record = db.session.query(ClassOpen).join(ClassInfo).filter(ClassInfo.user_id == self.user_id).all()
            # print(f"exclude_record={exclude_record}")
            exclude_id = [item.id for item in exclude_record]

            data = []
            for item in history:
                # f-string으로 임베딩할 텍스트를 생성
                data_string = f"tag: {item.ca_class_open.info.education_tag.genre}, title: {item.ca_class_open.info.title}"
    
                # 임베딩 생성
                embedding = self.openai_client.embeddings.create(
                    input=data_string,
                    model="text-embedding-3-small"
                ).data[0].embedding

                data.append(embedding)
            
            # 이전에 수강했던 클래스를 제외할 수 있도록 필터링 리스트 생성
            history_id = [item.ca_class_open.info.id for item in history] + exclude_id


            search = self.qdrant_client.search_batch(
                collection_name=self.detail_collection,
                requests=[
                    models.SearchRequest(
                        vector=vector,
                        limit=6, # 각 쿼리 벡터마다 10개의 결과를 가져옵니다.
                        filter=models.Filter(
                            must_not=[
                                models.FieldCondition(key="user_id", match=MatchValue(value=int(self.user_id))),
                                models.FieldCondition(key="is_full", match=MatchValue(value=True)),
                                models.FieldCondition(key="info_id",
                                                      match=models.MatchAny(
                                                          any=history_id
                                                      ))
                            ]
                        ),
                        with_payload=True
                    ) for vector in data
                ]
            )
        final_results = {}
        for result_list in search:
            for hit in result_list:
                info_id = hit.payload.get("info_id")
                if info_id is None:
                    continue
                # hit.id를 기준으로, 아직 없거나 더 높은 점수가 나왔을 때만 딕셔너리에 저장
                # if hit.id not in final_results or hit.score > final_results[hit.id].score:
                if info_id not in final_results or hit.score > final_results[info_id].score:

                    final_results[info_id] = hit

        # 3. 딕셔너리의 값들만 추출하여 점수(score) 기준으로 내림차순 정렬합니다.
        sorted_results = sorted(final_results.values(), key=lambda x: x.score, reverse=True)

        # 4. 최종적으로 정렬된 상위 N개의 결과를 사용합니다.
        top_10_results = sorted_results[:10]
        print(f"top_10_result={top_10_results}")
        
        if top_10_results is not None:
            return top_10_results
        else:
            raise RuntimeError(f"result={top_10_results}, 반환할 값이 없습니다.")
