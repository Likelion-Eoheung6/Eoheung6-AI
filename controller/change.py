from collections import OrderedDict
import json
from flask import Blueprint, Response, request
import openai
from pydantic import ValidationError

from common.response.success_response import SuccessResponse
from common.response.response_builder import ResponseBuilder
from custom_error.openai_connection_failed_error import OpenAIConnectionFailedError
from custom_error.openai_illegal_state import OpenAIIllegalStateError
from custom_error.openai_rate_limit import OpenAIRateLimitError
from service.data_embed import ChangeFlag


change_bp = Blueprint("change_is_full_glag", __name__, url_prefix="/ai")

@change_bp.route("/change", methods=["PATCH"])
def change_is_full_flag():
    info_id = request.json.get("infoId")
    is_full = request.json.get("isFull")

    body = OrderedDict([
            ("info_id", info_id),
            ("is_full", is_full)
        ])

    if(info_id is None or is_full is None):
        raise ValueError("None인 필드가 존재합니다.")
    
    change = ChangeFlag(info_id, is_full)
    try:
        change.change()
    except openai.APIConnectionError:
            raise OpenAIConnectionFailedError
    except openai.RateLimitError:
            raise OpenAIRateLimitError
    except openai.APIStatusError:
            raise OpenAIIllegalStateError
   
    result = [change.get_include_review(), change.get_without_review()]

    return Response(json.dumps(SuccessResponse.ok(result).convert(),
                               ensure_ascii=False, sort_keys=False),
                               200, mimetype="application/json")

    