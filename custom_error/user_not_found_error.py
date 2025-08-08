from common.error.base_error import BaseError
from custom_error.flask_error_code import FlaskErrorCode

class UserNotFoundError(BaseError):
    def __init__(self):
        super().__init__(FlaskErrorCode.MYSQL_USER_NOT_FOUND)