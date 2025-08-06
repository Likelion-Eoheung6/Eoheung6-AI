from flask import Blueprint, request, jsonify, Response
import json
from collections import OrderedDict
from service.data_embed import WithoutReview, IncludeReview
from controller.response_builder import ResponseBuilder

save_bp = Blueprint("save", __name__, url_prefix="/ai/save")


@save_bp.route("/includeReview", methods=["POST"])
def save_include_review():
      print("include_eview 컨트롤러 진입")
      try :
            body = OrderedDict([
            ("info_id", request.json.get("info_id")),
            ("title", request.json.get("title")),
            ("tag", request.json.get("tag")),
            ("user_id", request.json.get("user_id")),
            ("review", request.json.get("review")),
            ("is_full", request.json.get("is_full"))
            ])

            for value in list(body.values()):
                  # list(body.values())[0]
                  # list(body.values())[1] ...
                  if value is None:
                        raise ValueError
            
      except ValueError:
            return Response(json.dumps(
                        ResponseBuilder()
                        .is_success(False)
                        .code("FLASK_INVALID_REQUEST_400")
                        .http_status(400)
                        .message("info_id, title, tag, user_id, review, is_full은 모두 필수값입니다.")
                        .data(body)
                        .time_stamp()
                        .build(), ensure_ascii=False),
                        status=400,
                        mimetype="application/json")
      except UnboundLocalError as e:
            return Response(json.dumps(
                        ResponseBuilder()
                        .is_success(False)
                        .code("FLASK_INVALID_REQUEST_400")
                        .http_status(400)
                        .message("유효하지 않은 필드명입니다.")
                        .data(None)
                        .time_stamp()
                        .build(), ensure_ascii=False),
                        status=400,
                        mimetype="application/json")
    
      embed = IncludeReview(("info_id", request.json.get("info_id")),
                            ("title", request.json.get("title")),
                            ("tag", request.json.get("tag")),
                            ("user_id", request.json.get("user_id")),
                            ("review", request.json.get("review")),
                            ("is_full", request.json.get("is_full")))

      embed.save()
      
      return Response(json.dumps(
                  ResponseBuilder()
                  .is_success(True)
                  .code("FLASK_201")
                  .http_status(201)
                  .message("성공적으로 Qdrant Database에 저장되었습니다.")
                  .data(body)
                  .time_stamp()
                  .build(), ensure_ascii=False),
                  status=201,
                  mimetype="application/json")

@save_bp.route("/tag", methods=["POST"])
def save_tag():
      print("tag 컨트롤러 진입")
      try:
            body = OrderedDict([
            ("info_id", request.json.get("info_id")),
            ("tag", request.json.get("tag")),
            ("is_full", request.json.get("is_full"))
            ])

            for value in list(body.values()):
                  if value is None:
                        raise ValueError
      except ValueError:
            
            return Response(json.dumps(
                  ResponseBuilder()
                  .is_success(False)
                  .code("FLASK_INVALID_REQUEST_400")
                  .http_status(400)
                  .message("info_id, tag, is_full은 필수값입니다.")
                  .data(body)
                  .time_stamp()
                  .build()
            ), ensure_ascii=False,
            status=400,
            mimetype="application/json")
      except UnboundLocalError as e:
            
            return Response(json.dumps(
                  ResponseBuilder()
                  .is_success(False)
                  .code("FLASK_INVALID_REQUEST_400")
                  .http_status(400)
                  .message("유효하지 않은 필드명입니다.")
                  .data(body)
                  .time_stamp()
                  .build()
            ), ensure_ascii=False,
            status=400,
            mimetype="application/json")

      embed = WithoutReview(list(body.values())[0], list(body.values())[1], list(body.values())[2])

      embed.save()
      
      return Response(
            json.dumps(ResponseBuilder()
                       .is_success(True)
                       .code("FLASK_201")
                       .http_status(201)
                       .message("성공적으로 Qdrant Database에 저장되었습니다.")
                       .data(body)
                       .time_stamp()
                       .build(), ensure_ascii=False),
            status=201,
            mimetype="application/json"
      )