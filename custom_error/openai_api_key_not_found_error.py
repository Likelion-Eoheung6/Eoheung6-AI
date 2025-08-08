from common.error.base_error import BaseError
from custom_error.flask_error_code import FlaskErrorCode

class OpenAIApiKeyNotFoundError(BaseError):
    def __init__(self):
        super().__init__(FlaskErrorCode.OPENAI_API_KEY_NOT_FOUND)