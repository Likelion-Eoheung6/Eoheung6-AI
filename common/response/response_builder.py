
class ResponseBuilder:
    def __init__(self):
        self._data = {}
    
    def is_success(self, is_success: bool):
        self._data["isSuccess"] = is_success
        return self

    def code(self, code: str):
        self._data["code"] = code
        return self

    def http_status(self, http_status: int):
        self._data["httpStatus"] = http_status
        return self

    def message(self, message: str):
        self._data["message"] = message
        return self

    def data(self, data):
        self._data["data"] = data
        return self

    def time_stamp(self, time_stamp):
        self._data["timeStamp"] = time_stamp
        return self

    def build(self):
        return self._data
