from common.error.base_error import BaseError
from custom_error.flask_error_code import FlaskErrorCode

class QdrantConnectionFailedError(BaseError):
    def __init__(self):
        super().__init__(FlaskErrorCode.QDRANT_CONNECTION_FAILED)