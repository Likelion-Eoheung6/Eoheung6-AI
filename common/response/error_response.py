from typing import Generic, Optional, TypeVar

from common.response.base_response import BaseResponse
from common.response.code.base_response_code import BaseResponseCode
from common.response.response_builder import ResponseBuilder

T = TypeVar('T')

class ErrorResponse(Generic[T], BaseResponse):
    def __init__(self, data: T, base_response_code: BaseResponseCode, message: Optional[str]) -> 'ErrorResponse':
        if message is None:
            super().__init__(False, base_response_code.code, base_response_code.message)
        else:
            super().__init__(False, base_response_code.code, message)
        self.http_status = base_response_code.http_status
        self.data = data

    def at(self, base_response_code:BaseResponseCode) -> 'ErrorResponse':
        return ErrorResponse(None, base_response_code)

    def of(base_response_code: BaseResponseCode, data: Optional[T] = None, message: Optional[str] = None) -> 'ErrorResponse[T]':
        result_message = message if message is not None else base_response_code.message
        print(f"ErrorResponse={ErrorResponse}")
        return ErrorResponse(data, base_response_code, result_message)
    
    def convert(self):
        return ResponseBuilder().is_success(self.is_success).code(self.code).http_status(self.http_status).message(self.message).data(self.data).time_stamp(self.time_stamp).build()
    
    def toString(self):
        return f"isSuccess={self.is_success}, code={self.code}, httpStatus={self.http_status} message={self.message}, data={self.data}, timeStamp={self.time_stamp}"