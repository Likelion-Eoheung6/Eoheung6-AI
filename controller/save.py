from flask import Blueprint, request, jsonify, Response
import json
from collections import OrderedDict
from typing import Optional
from pydantic import BaseModel, ValidationError
from service.data_embed import TagAndClassDataEmbedding, ReviewDataEmbedding
import datetime
from controller.response_builder import ResponseBuilder

save_bp = Blueprint("save", __name__, url_prefix="/ai/save")

class SaveWithoutReviewReq(BaseModel):
      info_id: Optional[int]
      class_name: Optional[str]
      tag: Optional[list[str]]

      def getInfoId(self):
            return self.info_id
      def getTag(self):
            return self.tag
      def getClassName(self):
            return self.class_name
      
class SaveReview(BaseModel):
      info_id: int
      user_id: int
      review: str

      def getInfoId(self):
            return self.info_id
      def getUserId(self):
            return self.user_id
      def getReview(self):
            return self.review

@save_bp.route("/withoutReview", methods=["POST"])
def save_without_review():
      print("withoutReview 컨트롤러 진입")
      try :
            data = SaveWithoutReviewReq(**request.json)
      except ValidationError as e:
            body = OrderedDict([
            ("info_id", request.json.get("info_id")),
            ("class_name", request.json.get("class_name")),
            ("tag", request.json.get("tag"))
            ])
            return Response(json.dumps(
                        ResponseBuilder()
                        .is_success(False)
                        .code("FLASK_INVALID_REQUEST_400")
                        .http_status(400)
                        .message("info_id, tag, class_name은 모두 필수값입니다.")
                        .data(body)
                        .time_stamp()
                        .build(), ensure_ascii=False),
                        status=400,
                        mimetype="application/json")
      except UnboundLocalError as e:
            body = OrderedDict([
            ("info_id", request.json.get("info_id")),
            ("class_name", request.json.get("class_name")),
            ("tag", request.json.get("tag"))
            ])
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


      body = OrderedDict([
            ("info_id", data.getInfoId()),
            ("class_name", data.getClassName()),
            ("tag", data.getTag())
      ])
    
      embed = TagAndClassDataEmbedding()

      embed.save(data.getClassId(), data.getClassName(), data.getTag())
      
      
      
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

@save_bp.route("/review", methods=["POST"])
def save_review():
      print("review 컨트롤러 진입")
      try:
            data = SaveReview(**request.json)
      except ValidationError as e:
            body = OrderedDict([
            ("info_id", request.json.get("info_id")),
            ("user_id", request.json.get("user_id")),
            ("review", request.json.get("review"))
            ])
            return Response(json.dumps(
                  ResponseBuilder()
                  .is_success(False)
                  .code("FLASK_INVALID_REQUEST_400")
                  .http_status(400)
                  .message("info_id, user_id, review는 필수값입니다.")
                  .data(body)
                  .time_stamp()
                  .build()
            ), ensure_ascii=False,
            status=400,
            mimetype="application/json")
      except UnboundLocalError as e:
            body = OrderedDict([
            ("info_id", request.json.get("info_id")),
            ("user_id", request.json.get("user_id")),
            ("review", request.json.get("review"))
            ])
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

            
      body = OrderedDict([
            ("info_id", data.getInfoId()),
            ("user_id", data.getUserId()),
            ("review", data.getReview())
      ])

      embed = ReviewDataEmbedding()

      embed.save(data.getInfoId(), data.getUserId(), data.getReview())
      
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