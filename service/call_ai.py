from collections import OrderedDict
from service.config.sql_alchemy import db
from service.model.class_model import ClassInfo, ClassOpen
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
        is_open = ClassOpen.query.filter_by(info_id=id, is_full=False).first()
        if is_open is None:
            # 기간 만료 클래스일시
            # 재검색
            try:
                res = self.rag.re_call(id, tag, class_name, review)
                return res.payload
            except IndexError as e:
                return "죄송해요. 개설된 클래스 중, 어울리는 클래스가 없네요."
            
        # context로 정리
        context = OrderedDict([
            ("class_id", res['class_id']),
            ("class_name", res['class']),
            ("tag", res['tag'])])
        print(context)
        
        return context