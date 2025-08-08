from flask import Blueprint, jsonify, request, Response
import json
from collections import OrderedDict
from common.constant import StaticValue
from common.response.error_response import ErrorResponse
from common.response.success_response import SuccessResponse
from common.response.response_builder import ResponseBuilder
from controller.jwt_parser import JwtParser, JwtDecorder
from custom_error.user_not_found_error import UserNotFoundError
from service.rag import RagAnswer
from service.config.sql_alchemy import db
from service.model.class_model import User


call_bp = Blueprint("get_answer", __name__, url_prefix="/ai")

@call_bp.route("/call", methods=["GET"])
def save_data():
      print("save_data 컨트롤러 호출")
      token = JwtDecorder(JwtParser(request).parse()).decode()
      login_user_id = token['id']

      query = db.session.query(User.user_id).filter(User.id == login_user_id).first()
      if query:
            user_id = query[0]
            user_id = int(user_id)


      call = RagAnswer(user_id)
      
      res = call.call()
      
      result = [item.payload.get("info_id") for item in res]
      print(f"top_10_info_id={result}")

      # error_response = ErrorResponse.of(e.base_response_code)
      # return jsonify(error_response.convert()), e.base_response_code.http_status

      return Response(json.dumps(SuccessResponse.ok(result).convert(), ensure_ascii=False),
                        status = 200,
                        mimetype="application/json")