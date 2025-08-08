from common.response.code.base_response_code import BaseResponseCode

class BaseError(Exception):
    def __init__(self, base_response_code: BaseResponseCode):
        self.base_response_code = base_response_code
        super().__init__(base_response_code.message)