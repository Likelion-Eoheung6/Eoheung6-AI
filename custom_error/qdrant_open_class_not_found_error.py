from common.error.base_error import BaseError
from custom_error.flask_error_code import FlaskErrorCode

class QdrantOpenClassNotFoundError(BaseError):
    def __init__(self):
        super().__init__(FlaskErrorCode.QDRANT_OPEN_CLASS_NOT_FOUND)