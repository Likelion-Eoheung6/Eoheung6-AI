from flask import Blueprint, request, Response
import json

import openai
from common.response.success_response import SuccessResponse
from controller.jwt_parser import JwtParser, JwtDecorder
from custom_error.openai_connection_failed_error import OpenAIConnectionFailedError
from custom_error.openai_illegal_state import OpenAIIllegalStateError
from custom_error.openai_rate_limit import OpenAIRateLimitError
from service.rag import RagAnswer
from common.config.sql_alchemy import db
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
      try:
            res = call.call()
      except openai.APIConnectionError:
            raise OpenAIConnectionFailedError()
      except openai.RateLimitError:
            raise OpenAIRateLimitError()
      except openai.APIStatusError:
            raise OpenAIIllegalStateError()
      
      result = [item.payload.get("info_id") for item in res]


      return Response(json.dumps(SuccessResponse.ok(result).convert(), ensure_ascii=False, sort_keys=False),
                        status = 200,
                        mimetype="application/json")