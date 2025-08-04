from flask import Blueprint, request, jsonify, Response
import json
from collections import OrderedDict
from service.data_embed import TagAndClassDataEmbedding, ReviewDataEmbedding
import datetime

save_bp = Blueprint("rcmd", __name__, url_prefix="/ai/save")


@save_bp.route("/withoutReview", methods=["POST"])
def save_data():
      print("withoutReview 컨트롤러 진입")
      class_id = request.json.get("class_id")
      # user_id = request.json.get("user_id")
      tag = request.json.get("tag")
      class_name = request.json.get("class")
      # 리뷰는 다른 컨트롤러에서 컨트롤할 예정
      # review = request.json.get("review")


      body = OrderedDict([
            ("class_id", class_id),
            ("tag", tag),
            ("class_name", class_name),
      ])
    
      embed = TagAndClassDataEmbedding()

      embed.save(class_id, tag, class_name)
      
      response_data = {
            "isSuccess": True,
            "code": "201",
            "httpStatus": 201,
            "message": "성공적으로 Qdrant Database에 저장되었습니다.",
            "data": body,
            "timeStamp": datetime.datetime.now().isoformat()
      }

      
      return Response(
            json.dumps(response_data, ensure_ascii=False),
            status=201,
            mimetype="application/json"
      )

@save_bp.route("/review", methods=["POST"])
def save_data():
      print("review 컨트롤러 진입")

      class_id = request.json.get("class_id")
      user_id = request.json.get("user_id")
      review = request.json.get("review")

      body = OrderedDict([
            ("class_id", class_id),
            ("user_id", user_id),
            ("review", review)
      ])

      embed = ReviewDataEmbedding()

      embed.save(class_id, user_id, review)

      response_data = {
            "isSuccess": True,
            "code": "201",
            "httpStatus": 201,
            "message": "성공적으로 Qdrant Database에 저장되었습니다.",
            "data": body,
            "timeStamp": datetime.datetime.now().isoformat()
      }

      
      return Response(
            json.dumps(response_data, ensure_ascii=False),
            status=201,
            mimetype="application/json"
      )