from flask import Blueprint, request, jsonify, Response
import json
from collections import OrderedDict
from typing import Optional
from pydantic import BaseModel, ValidationError
from service.data_embed import TagAndClassDataEmbedding, ReviewDataEmbedding
import datetime
from controller.response_builder import ResponseBuilder

save_bp = Blueprint("rcmd", __name__, url_prefix="/ai/save")

class SaveWithoutReviewReq(BaseModel):
      class_id: Optional[int]
      class_name: Optional[str]
      tag: Optional[list[str]]

      def getClassId(self):
            return self.class_id
      def getTag(self):
            return self.tag
      def getClassName(self):
            return self.class_name
      
class SaveReview(BaseModel):
      class_id: int
      user_id: int
      review: str

      def getClassId(self):
            return self.class_id
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
            ("class_id", request.json.get("class_id")),
            ("class_name", request.json.get("class_name")),
            ("tag", request.json.get("tag"))
            ])
            return Response(json.dumps(
                        ResponseBuilder()
                        .is_success(False)
                        .code("Flask_Invalid_Request_400")
                        .http_status(400)
                        .message("class_id, tag, class_name은 모두 필수값입니다.")
                        .data(body)
                        .time_stamp()
                        .build(), ensure_ascii=False),
                        status=400,
                        mimetype="application/json")
      except UnboundLocalError as e:
            body = OrderedDict([
            ("class_id", request.json.get("class_id")),
            ("class_name", request.json.get("class_name")),
            ("tag", request.json.get("tag"))
            ])
            return Response(json.dumps(
                        ResponseBuilder()
                        .is_success(False)
                        .code("Flask_Invalid_Request_400")
                        .http_status(400)
                        .message("유효하지 않은 필드명입니다.")
                        .data(None)
                        .time_stamp()
                        .build(), ensure_ascii=False),
                        status=400,
                        mimetype="application/json")


      body = OrderedDict([
            ("class_id", data.getClassId()),
            ("class_name", data.getClassName()),
            ("tag", data.getTag())
      ])
    
      embed = TagAndClassDataEmbedding()

      embed.save(data.getClassId(), data.getClassName(), data.getTag())
      
      
      
      return Response(json.dumps(
                  ResponseBuilder()
                  .is_success(True)
                  .code("Flask_201")
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
            ("class_id", request.json.get("class_id")),
            ("user_id", request.json.get("user_id")),
            ("review", request.json.get("review"))
            ])
            return Response(json.dumps(
                  ResponseBuilder()
                  .is_success(False)
                  .code("Flask_Invalid_Request_400")
                  .http_status(400)
                  .message("class_id, user_id, review는 필수값입니다.")
                  .data(body)
                  .time_stamp()
                  .build()
            ), ensure_ascii=False,
            status=400,
            mimetype="application/json")
      except UnboundLocalError as e:
            body = OrderedDict([
            ("class_id", request.json.get("class_id")),
            ("user_id", request.json.get("user_id")),
            ("review", request.json.get("review"))
            ])
            return Response(json.dumps(
                  ResponseBuilder()
                  .is_success(False)
                  .code("Flask_Invalid_Request_400")
                  .http_status(400)
                  .message("유효하지 않은 필드명입니다.")
                  .data(body)
                  .time_stamp()
                  .build()
            ), ensure_ascii=False,
            status=400,
            mimetype="application/json")

            
      body = OrderedDict([
            ("class_id", data.getClassId()),
            ("user_id", data.getUserId()),
            ("review", data.getReview())
      ])

      embed = ReviewDataEmbedding()

      embed.save(data.getClassId(), data.getUserId(), data.getReview())
      
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