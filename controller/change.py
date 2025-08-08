from collections import OrderedDict
import json
from flask import Blueprint, Response, request
from pydantic import ValidationError

from common.response.success_response import SuccessResponse
from common.response.response_builder import ResponseBuilder
from service.data_embed import ChangeFlag


change_bp = Blueprint("change_is_full_glag", __name__, url_prefix="/ai")

@change_bp.route("/change", methods=["POST"])
def change_is_full_flag():
    info_id = request.json.get("info_id")
    is_full = request.json.get("is_full")

    body = OrderedDict([
            ("info_id", info_id),
            ("is_full", is_full)
        ])

    if(info_id is None or is_full is None):
        raise ValidationError
    
    change = ChangeFlag(info_id, is_full)
    change.change()
   
    # return SuccessResponse.ok

    return Response(json.dumps(ResponseBuilder()

                               .is_success(True)
                               .code("FLASK_201")
                               .http_status(201)
                               .message("성공적으로 Qdrant Database에서 is_full 필드 값이 변경되었습니다.")
                               .data([change.get_include_review(), change.get_without_review()])
                               .time_stamp()
                               .build(), ensure_ascii=False),
                               status=201,
                               mimetype="application/json")

