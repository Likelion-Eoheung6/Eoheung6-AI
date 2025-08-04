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
            # id를 MySQL에 재검색
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

        # prompt 생성
        prompt = ("사용자는 " + self.rag.sentence(tag, class_name, review) +
                  "클래스를 좋아해서" + context +
                  "\n 이 클래스가 추천됐어. 이 클래스가 추천된 이유를 5줄 내외로 알려줘. 바로 본문부터 시작해야 해. 대답 없이.")
        
        # 답변 반환
        return openai_client.chat.completions.create(
            model="gpt-4o-2024-05-13",
            messages=[
                {"role": "system", "content": "당신은 친절하게 사용자의 정보를 바탕으로 클래스를 추천해주는 추천 도우미입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        ).choices[0].message.content