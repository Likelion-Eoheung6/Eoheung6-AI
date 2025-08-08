from typing import Optional, Union
from common.response.code.base_response_code import BaseResponseCode
from datetime import datetime

class BaseResponse:
    def __init__(self, is_success: bool, code: str, message: str):
        self.is_success = is_success
        self.code = code
        self.message = message
        self.time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # is_success만 매개변수 초기화, code는 BaseResponseCode로 넘김
    @staticmethod
    def of(is_success: bool, code_or_base: Union[str, BaseResponseCode], message: Optional[str] = None) -> 'BaseResponse':
        if isinstance(code_or_base, BaseResponseCode):
            code = code_or_base.code
            msg = message if message is not None else code_or_base.message
        else:
            code = code_or_base
            msg = message if message is not None else ""

        return BaseResponse(is_success, code, msg)
