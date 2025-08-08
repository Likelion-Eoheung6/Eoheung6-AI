from common.error.base_error import BaseError
from custom_error.flask_error_code import FlaskErrorCode

class QdrantInfoIdNotFoundError(BaseError):
    def __init__(self):
        super().__init__(FlaskErrorCode.QDRANT_INFO_ID_NOT_FOUND)