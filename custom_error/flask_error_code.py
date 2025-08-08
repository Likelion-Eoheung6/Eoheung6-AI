from enum import Enum

from common.response.code.base_response_code import BaseResponseCode, Basic

class FlaskErrorCode(BaseResponseCode, Basic):
    MYSQL_USER_NOT_FOUND = ("USER_NOT_FOUND_404", 404, "해당 login_id를 사용하는 사용자를 찾을 수 없습니다.")
    QDRANT_OPEN_CLASS_NOT_FOUND = ("QDRANT_OPEN_CLASS_NOT_FOUND_404", 404, "Qdrant 데이터베이스에 현재 is_full=false인 클래스가 없습니다.")
    OPENAI_API_KEY_NOT_FOUND = ("OPENAI_API_KEY_NOT_FOUND_404", 404, "Open API Key를 찾을 수 없습니다.")
    QDRANT_CONNECTION_FAILED = ("QDRANT_CONNECTION_FAILED_503", 503, "Qdarnt Database와 연결에 실패했습니다.")
    QDRANT_INFO_ID_NOT_FOUND = ("QDRANT_INFO_ID_NOT_FOUND_404", 404, "해당 info_id의 노드를 조회할 수 없습니다.")
    OPENAI_CONNECTION_FAILED = ("OPENAI_CONNECTION_FAILED_503", 503, "OpenAI API 서버와의 연결에 실패했습니다.")
    OPENAI_RATE_LIMIT = ("OPENAI_RATE_LIMIT_402", 402, "API Key의 금일 허용 한도 넘는 요청입니다.")

    def __init__(self, code, http_status, message):
        self._code = code
        self._http_status = http_status
        self._message = message

    @property
    def code(self) -> str:
        return self._code
    
    @property
    def http_status(self) -> int:
        return self._http_status
    
    @property
    def message(self) -> str:
        return self._message
    