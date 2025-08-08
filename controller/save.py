from flask import Blueprint, request, jsonify, Response
import json
from collections import OrderedDict

from pydantic import ValidationError
from common.constant import StaticValue
from common.response.success_response import SuccessResponse
from service.data_embed import WithoutReview, IncludeReview
from common.response.response_builder import ResponseBuilder

save_bp = Blueprint("save", __name__, url_prefix="/ai/save")


@save_bp.route("/includeReview", methods=["POST"])
def save_include_review():
      print("include_eview 컨트롤러 진입")
      body = OrderedDict([
            ("info_id", request.json.get("info_id")),
            ("title", request.json.get("title")),
            ("tag", request.json.get("tag")),
            ("is_full", request.json.get("is_full"))
      ])

      for value in list(body.values()):
            if value is None:
                  raise ValidationError
            
      embed = IncludeReview(("info_id", request.json.get("info_id")),
                            ("title", request.json.get("title")),
                            ("tag", request.json.get("tag")),
                            ("user_id", request.json.get("user_id")),
                            ("review", request.json.get("review")),
                            ("is_full", request.json.get("is_full")))

      result = embed.save()
      
      return Response(json.dumps(SuccessResponse.created(result).convert(), ensure_ascii=False, sort_keys=False),
                      201, mimetype="application/json")


@save_bp.route("/tag", methods=["POST"])
def save_tag():
      print("tag 컨트롤러 진입")
      body = OrderedDict([
            ("info_id", request.json.get("info_id")),
            ("tag", request.json.get("tag")),
            ("is_full", request.json.get("is_full"))
            ])

      for value in list(body.values()):
            if value is None:
                  raise ValidationError
            
      embed = WithoutReview(list(body.values())[0], list(body.values())[1], list(body.values())[2])

      result = embed.save()

      return Response(json.dumps(SuccessResponse.created(result).convert(), ensure_ascii=False, sort_keys=False), status = 201, mimetype="application/json")