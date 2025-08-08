from common.error.base_error import BaseError
from custom_error.flask_error_code import FlaskErrorCode

class OpenAIIllegalStateError(BaseError):
    def __init__(self):
        super().__init__(FlaskErrorCode.OPENAI_ILLEGAL_STATE_ERROR)