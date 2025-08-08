from typing import Generic, Optional, TypeVar

from common.response.base_response import BaseResponse
from common.response.code.base_response_code import BaseResponseCode
from common.response.code.success_response_code import SuccessResponseCode
from common.response.response_builder import ResponseBuilder

T = TypeVar('T')

class SuccessResponse(Generic[T], BaseResponse):
    def __init__(self, data: T, base_response_code: BaseResponseCode) -> 'SuccessResponse':
        super().__init__(True, base_response_code.code, base_response_code.message)
        self.http_status = base_response_code.http_status
        self.data = data
    
    def ok(data: T) -> 'SuccessResponse[T]':
        return SuccessResponse(data, SuccessResponseCode.SUCCESS_OK)
    
    def created(data: T) -> 'SuccessResponse[T]':
        return SuccessResponse(data, SuccessResponseCode.SUCCESS_CREATED)
    
    def empty() -> 'SuccessResponse':
        return SuccessResponse(None, SuccessResponseCode.SUCCESS_OK)
    
    def of(data: T, base_response_code: BaseResponseCode) -> 'SuccessResponse[T]':
        return SuccessResponse(data, base_response_code)
    
    def at(base_response_code: BaseResponseCode, data: Optional[T]) -> 'SuccessResponse[T]':
        if data is None:
            return SuccessResponse(None, base_response_code)
        else:
            return SuccessResponse(data, base_response_code)

    def convert(self):
        return ResponseBuilder().is_success(self.is_success).code(self.code).http_status(self.http_status).message(self.message).data(self.data).time_stamp(self.time_stamp).build()