from common.constant.StaticValue import StaticValue
from common.response.code.base_response_code import BaseResponseCode, Basic


class ErrorResponseCode(BaseResponseCode, Basic):
    def __init__(self, code: str, http_status: int, message: str):
        self._code = code
        self._http_status = http_status
        self._message = message

    BAD_REQUEST_ERROR = ("GLOBAL_400_1", StaticValue.BAD_REQUEST, "잘못된 요청입니다.")
    INVALID_HTTP_MESSAGE_BODY = ("GLOBAL_400_2", StaticValue.BAD_REQUEST, "HTTP 요청 바디의 형식이 잘못되었습니다.")
    INVALID_HTTP_MESSAGE_PARAMETER = ("GLOBAL_400_2", StaticValue.BAD_REQUEST, "HTTP 요청 파라미터 형식이 잘못되었습니다.")
    UNAUTHORIZED_TOKEN = ("GLOBAL_401_1", StaticValue.UNAUTHORIZED, "토큰이 만료되거나, 유효하지 않은 시그니처입니다.")
    ACCESS_DENIED_REQUEST = ("GLOBAL_403", StaticValue.FORBIDDEN, "해당 요청에 접근 권한이 없습니다.")
    NOT_FOUND_ENDPOINT = ("GLOBAL_404", StaticValue.NOT_FOUND,"존재하지 않는 엔드포인트입니다. 요청 URL을 확인해주세요.")
    UNSUPPORTED_HTTP_METHOD = ("GLOBAL_405", StaticValue.METHOD_NOT_ALLOWED, "지원하지 않는 HTTP 메소드입니다.")
    INTERNAL_SERVER_ERROR = ("GLOBAL_500", StaticValue.INTERNAL_SERVER_ERROR, "서버 내부에서 알 수 없는 에러가 발생했습니다.")
    SERVICE_UNAVAILABLE = ("GLOBAL_503", StaticValue.SERVICE_UNAVAILABLE, "외부 API와 연동에 실패했습니다.")

    @property
    def code(self) -> str:
        return self._code

    @property
    def http_status(self) -> int:
        return self._http_status

    @property
    def message(self) -> str:
        return self._message