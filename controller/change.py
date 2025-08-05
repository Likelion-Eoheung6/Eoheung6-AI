
from collections import OrderedDict
import json
from flask import Blueprint, Response, request
from pydantic import ValidationError

from controller.response_builder import ResponseBuilder
from service.data_embed import ChangeFlag


call_bp = Blueprint("get_answer", __name__, url_prefix="/ai")

@call_bp.route("/call", methods=["POST"])
def change_is_full_flag():
    info_id = request.json.get("info_id")
    is_full = request.json.get("is_full")

    body = OrderedDict([
            ("info_id", info_id),
            ("is_full", is_full)
        ])

    try:
        if(info_id is None or is_full is None):
            raise ValidationError
    except:
        return Response(json.dumps(
            ResponseBuilder()
            .is_success(False)
            .code("FLASK_INVALID_REQUEST_400")
            .http_status(400)
            .message("info_id, is_full은 필수값입니다.")
            .data(body)
            .time_stamp()
            .build()
        ), ensure_ascii=False,
        status=400,
        mimetype="application/json")
    
    change = ChangeFlag(info_id, is_full)

    change.change()

    return Response(json.dumps(ResponseBuilder()
                               .is_success(True)
                               .code(FLASK_201)
                               .http_status(201)
                               .message("성공적으로 Qdrant Database에서 is_full 필드 값이 변경되었습니다.")
                               .data(change.get())
                               .time_stamp()
                               .build), ensure_ascii=False,
                               status=201,
                               mimetype="application/json")

    