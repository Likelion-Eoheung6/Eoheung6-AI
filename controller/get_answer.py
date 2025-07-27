from flask import Blueprint, request, Response
import json
from collections import OrderedDict
from service.rag import RagAnswer
import datetime


call_bp = Blueprint("get_answer", __name__, url_prefix="/ai")

@call_bp.route("/call", methods=["POST"])
def save_data():
    call = RagAnswer()

    tag = request.json.get("tag")
    class_name = request.json.get("class")
    review = request.json.get("review")

    body = OrderedDict([
            ("tag", tag),
            ("class_name", class_name),
            ("review", review)
      ])

    res = call.call(tag, class_name, review)

    response_data = {
            "isSuccess": True,
            "code": "FLASK_200",
            "httpStatus": 200,
            "message": "RAG 검색 결과입니다.",
            "data": res,
            "timeStamp": datetime.datetime.now().isoformat()
      }
    return Response(
            json.dumps(response_data, ensure_ascii=False),
            status=200,
            mimetype="application/json"
      )