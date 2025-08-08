class StaticValue:
    OK = 200
    CREATED = 201

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409

    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

    # # 2xx
    # @property
    # def OK(self) -> int:
    #     return self.OK
    
    # @property
    # def CREATED(self) -> int:
    #     return self.CREATED
    
    # # 4xx
    # @property
    # def BAD_REQUEST(self) -> int:
    #     return self.BAD_REQUEST
    # @property
    # def UNAUTHORIZED(self) -> int:
    #     return self.UNAUTHORIZED
    # @property
    # def FORBIDDEN(self) -> int:
    #     return self.FORBIDDEN
    # @property
    # def NOT_FOUND(self) -> int:
    #     return self.NOT_FOUND
    # @property
    # def METHOD_NOT_ALLOWED(self) -> int:
    #     return self.METHOD_NOT_ALLOWED
    # @property
    # def CONFLICT(self) -> int:
    #     return self.CONFLICT
    
    # # 5xx
    # @property
    # def INTERNAL_SERVER_ERROR(self) -> int:
    #     return self.INTERNAL_SERVER_ERROR
    # @property
    # def SERVICE_UNAVAILABLE(self) -> int:
    #     return self.SERVICE_UNAVAILABLE