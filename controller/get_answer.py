from flask import Blueprint, request, Response
import json
from collections import OrderedDict
from controller.response_builder import ResponseBuilder
from controller.jwt_parser import JwtParser, JwtDecorder
from service.rag import RagAnswer
from service.config.sql_alchemy import db
from service.model.class_model import User


call_bp = Blueprint("get_answer", __name__, url_prefix="/ai")

@call_bp.route("/call", methods=["POST"])
def save_data():
      # user_id = request.json.get("user_id")
      token = JwtDecorder(JwtParser(request).parse()).decode()
      print(token)
      login_user_id = token['id']
      print(login_user_id)

      query = db.session.query(User.user_id).filter(User.id == login_user_id).first()
      if query:
            user_id = query[0]
            user_id = int(user_id)

      print(user_id)
      tag = request.json.get("tag")
      title = request.json.get("title")
      review = request.json.get("review")

      body = OrderedDict([
           ("tag", tag),
           ("title", title),
           ("review", review)
      ])

      call = RagAnswer(user_id, tag, title, review)
      try:
            res = call.call()
      except ValueError as e:
            return Response(
            json.dumps(ResponseBuilder()
                       .is_success(False)
                       .code("QDRANT_404")
                       .http_status(404)
                       .message("RAG 검색 결과입니다.")
                       .data(str(e))
                       .time_stamp()
                       .build(), ensure_ascii=False),
                        status=404,
                        mimetype="application/json"
      )
      result = [point.payload.get("info_id") for point in res]

      return Response(
            json.dumps(ResponseBuilder()
                       .is_success(200)
                       .code("FLASK_200")
                       .http_status(200)
                       .message("RAG 검색 결과입니다.")
                       .data(result)
                       .time_stamp()
                       .build(), ensure_ascii=False),
                        status=200,
                        mimetype="application/json"
      )