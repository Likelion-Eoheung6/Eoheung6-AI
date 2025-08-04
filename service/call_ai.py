from service.config.sql_alchemy import db
from service.model.class_model import Class, ClassOpen
from service.rag import RagAnswer
from service.config.qdrant_config import openai_client

class ResAI:
    def __init__(self):
        self.db = db
        self.rag = RagAnswer()

    def getAIRes(self, tag: str, class_name: str, review: str):
        res = self.rag.call(tag, class_name, review)

        id = res.get("class_id")
        print(id)
            # id를 MySQL에 검색
        is_open = ClassOpen.query.filter_by(class_id=id).first()
        if is_open is None:
            # 기간 만료 클래스일시
            # 재검색
            try:
                res = self.rag.re_call(id, tag, class_name, review)
                return res.payload
            except IndexError as e:
                return "죄송해요. 개설된 클래스 중, 어울리는 클래스가 없네요."
            
        # context로 정리
        context = (
            f"추천된 클래스 정보입니다:\n"
            f"- 카테고리(태그): {res['tag']}\n"
            f"- 클래스명: {res['class']}\n"
            f"- 수강자 리뷰: \"{res['review']}\"\n"
        )

        # # prompt 생성
        # prompt = ("사용자는 " + self.rag.sentence(tag, class_name, review) +
        #           "클래스를 좋아해서" + context +
        #           "\n 이 클래스가 추천됐어. 이 클래스가 추천된 이유를 5줄 내외로 알려줘. 바로 본문부터 시작해야 해. 대답 없이.")
        
        # 답변 반환
        return context