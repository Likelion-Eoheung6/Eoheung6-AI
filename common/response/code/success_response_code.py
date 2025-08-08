
from common.response.code.base_response_code import BaseResponseCode, Basic
from common.constant.StaticValue import StaticValue

class SuccessResponseCode(BaseResponseCode, Basic):
    def __init__(self, code: str, http_status: int, message: str):
        self._code = code
        self._http_status = http_status
        self._message = message
        
    SUCCESS_OK = ("SUCCESS_200", StaticValue.OK, "호출에 성공햇습니다")
    SUCCESS_CREATED = ("SUCCESS_201", StaticValue.CREATED, "호출에 성공하였습니다.")

    @property
    def code(self) -> str:
        return self._code

    @property
    def http_status(self) -> int:
        return self._http_status

    @property
    def message(self) -> str:
        return self._message