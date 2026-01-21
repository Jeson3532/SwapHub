class ResponseStatus:
    class SuccessResponse:
        def __init__(self, status_code=200, detail=None):
            self.status_code = status_code
            self.detail = detail

    class FailedResponse:
        def __init__(self, status_code=400, detail=None):
            self.status_code = status_code
            self.detail = detail

