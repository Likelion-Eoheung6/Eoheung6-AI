import datetime

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

    def data(self, data1, data2 = None):
        if data2 is None:
            self._data["data1"] = data1
            return self
        else:
            self._data["data1"] = data1
            self._data["data2"] = data2
            return [data1, data2]

    def time_stamp(self):
        self._data["timeStamp"] = datetime.datetime.now().isoformat()
        return self

    def build(self):
        return self._data
