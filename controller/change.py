import json
from flask import Blueprint, Response, request
import openai

from common.response.code.base_response_code import BaseResponseCode
from common.response.code.error_response_code import ErrorResponseCode
from common.response.success_response import SuccessResponse
from common.response.error_response import ErrorResponse
from custom_error.openai_connection_failed_error import OpenAIConnectionFailedError
from custom_error.openai_illegal_state import OpenAIIllegalStateError
from custom_error.openai_rate_limit import OpenAIRateLimitError
from service.data_embed import ChangeFlag


change_bp = Blueprint("change_is_full_glag", __name__, url_prefix="/ai")

@change_bp.route("/change", methods=["PATCH"])
def change_is_full_flag():
    items_to_change = request.get_json()

    if isinstance(items_to_change, dict):
          items_to_change = [items_to_change]

    if not isinstance(items_to_change, list):
          return Response(json.dumps(ErrorResponse.at(ErrorResponseCode.INVALID_HTTP_MESSAGE_BODY).convert(),
                                     ensure_ascii=False, sort_keys=False), 400, mimetype="application/json")

    results = []
    errors = []

    for item in items_to_change:
          info_id = item.get("infoId")
          is_full = item.get("isFull")

          print(info_id)
          print,(is_full)
        
          if not isinstance(info_id, int) or not isinstance(is_full, bool):
                print("잘못된 Request DTO 양식입니다.")
                errors.append({"item": item, "message": "Message Body의 형식이 잘못되었습니다."})
                continue
          
          try:
                change_flag = ChangeFlag(
                      info_id,
                      is_full
                )
                change_flag.execute()
                results.append({
                      "infoId": info_id,
                      "isFull": is_full,
                })
          except Exception as e:
                errors.append({
                      "infoId": info_id,
                      "message": str(e)
                })
    
    status_code = 200 if not errors else 400

    return Response(json.dumps(SuccessResponse.ok([results, errors]).convert(),
                               ensure_ascii=False, sort_keys=False),
                               status_code, mimetype="application/json")

    