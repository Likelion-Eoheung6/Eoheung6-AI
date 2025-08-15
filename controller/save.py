from flask import Blueprint, request, Response
import json
from collections import OrderedDict

import openai
from pydantic import ValidationError
from common.response.success_response import SuccessResponse
from custom_error.openai_connection_failed_error import OpenAIConnectionFailedError
from custom_error.openai_illegal_state import OpenAIIllegalStateError
from custom_error.openai_rate_limit import OpenAIRateLimitError
from service.data_embed import WithoutReview, IncludeReview

save_bp = Blueprint("save", __name__, url_prefix="/ai/save")


@save_bp.route("/detail", methods=["POST"])
def save_include_review():
      print("include_review 컨트롤러 진입")
      print(request.get_json())
      body = OrderedDict([
            ("info_id", request.json.get("infoId")),
            ("title", request.json.get("title")),
            ("tag", request.json.get("tag")),
            ("is_full", request.json.get("isFull"))
      ])

      for value in list(body.values()):
            print(value)
            if value is None:
                  raise ValueError("값이 None인 필드가 존재합니다.")

      embed = IncludeReview(request.json.get("infoId"),
                            request.json.get("title"),
                            request.json.get("tag"),
                            request.json.get("isFull"))

      try:
            result = embed.save()
      except openai.APIConnectionError:
            raise OpenAIConnectionFailedError()
      except openai.RateLimitError:
            raise OpenAIRateLimitError()
      except openai.APIStatusError:
            raise OpenAIIllegalStateError()
      
      return Response(json.dumps(SuccessResponse.created(result).convert(), ensure_ascii=False, sort_keys=False),
                      201, mimetype="application/json")


@save_bp.route("/tag", methods=["POST"])
def save_tag():
      print("tag 컨트롤러 진입")
      body = OrderedDict([
            ("info_id", request.json.get("infoId")),
            ("tag", request.json.get("tag")),
            ("is_full", request.json.get("isFull"))
            ])

      for value in list(body.values()):
            if value is None:
                  raise ValidationError
            
      embed = WithoutReview(list(body.values())[0], list(body.values())[1], list(body.values())[2])
      try:
            result = embed.save()
      except openai.APIConnectionError:
            raise OpenAIConnectionFailedError()
      except openai.RateLimitError:
            raise OpenAIRateLimitError()
      except openai.APIStatusError:
            raise OpenAIIllegalStateError()
      

      return Response(json.dumps(SuccessResponse.created(result).convert(), ensure_ascii=False, sort_keys=False), status = 201, mimetype="application/json")