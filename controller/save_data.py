from flask import Blueprint, request, jsonify, Response
import json
from collections import OrderedDict
from service.data_embed import DataEmbedding
import datetime

save_bp = Blueprint("rcmd", __name__, url_prefix="/ai")

@save_bp.route("/save", methods=["POST"])
def save_data():

      user_id = request.json.get("user_id")
      tag = request.json.get("tag")
      class_name = request.json.get("class")
      review = request.json.get("review")


      body = OrderedDict([
            ("user_id", user_id),
            ("tag", tag),
            ("class_name", class_name),
            ("review", review)
      ])
    
      embed = DataEmbedding()

      embed.save(tag, class_name, review)
      
      response_data = {
            "isSuccess": True,
            "code": "FLASK_201",
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