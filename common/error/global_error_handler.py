
from jwt import ExpiredSignatureError ,InvalidTokenError
from common.error.base_error import BaseError
from common.response.code.error_response_code import ErrorResponseCode
from common.response.error_response import ErrorResponse
from flask import Response, json
from pydantic import ValidationError
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest, Unauthorized


def GlobalErrorHandler(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        error_response = ErrorResponse.of(
            ErrorResponseCode.INVALID_HTTP_MESSAGE_BODY, e.errors()[0]['msg']
        )
        return Response(json.dumps(error_response.convert(), ensure_ascii=False, sort_kes = False), status = error_response.http_status, mimetype="application/json")
    
    @app.errorhandler(404)
    @app.errorhandler(NotFound)
    def handle_not_found(e):
        error_response = ErrorResponse.of(ErrorResponseCode.INVALID_HTTP_MESSAGE_BODY)
        return Response(json.dumps(error_response.convert(), ensure_ascii=False, sort_kes = False), status = error_response.http_status, mimetype="application/json")
    
    @app.errorhandler(405)
    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(e):
        error_response = ErrorResponse.of(ErrorResponseCode.UNSUPPORTED_HTTP_METHOD)
        return Response(json.dumps(error_response.convert(), ensure_ascii=False, sort_kes = False), status = error_response.http_status, mimetype="application/json")
    
    @app.errorhandler(400)
    @app.errorhandler(BadRequest)
    def handler_bad_request(e):
        error_response = ErrorResponse.of(ErrorResponseCode.BAD_REQUEST_ERROR)
        return Response(json.dumps(error_response.convert(), ensure_ascii=False, sort_kes = False), status = error_response.http_status, mimetype="application/json")
    
    @app.errorhandler(401)
    @app.errorhandler(Unauthorized)
    def handle_unauthorized_request(e):
        error_response = ErrorResponse.of(ErrorResponseCode.UNAUTHORIZED_TOKEN)
        return Response(json.dumps(error_response.convert(), ensure_ascii=False, sort_kes = False), status = error_response.http_status, mimetype="application/json")
    
    @app.errorhandler(ExpiredSignatureError)
    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token(e):
        error_response = ErrorResponse.of(ErrorResponseCode.UNAUTHORIZED_TOKEN)
        return Response(json.dumps(error_response.convert(), ensure_ascii=False, sort_keys=False), status = error_response.http_status, mimetype="application/json")
    

    @app.errorhandler(BaseError)
    def handle_unauthorized_request(e: BaseError):
        error_response = ErrorResponse.at(e.base_response_code.code)
        return Response(json.dumps(error_response.convert(), ensure_ascii=False, sort_keys=False), status = error_response.http_status, mimetype="application/json")
    
    @app.errorhandler(401)
    @app.errorhandler(Unauthorized)
    def handle_unauthorized_request(e):
        error_response = ErrorResponse.of(ErrorResponseCode.UNAUTHORIZED_TOKEN)
        return Response(json.dumps(error_response.convert(), ensure_ascii=False), status = error_response.http_status, mimetype="application/json")