from rest_framework.response import Response


class SuccessResponse(Response):
    """
    Request proceed successfully
    """
    def __init__(self, data=None, status=200, **kwargs):
        data['success'] = True
        super().__init__(data=data, status=status, **kwargs)


class FailureResponse(Response):
    """
    Request proceed successfully but the response wasn't as it expected
    """
    def __init__(self, data=None, status=200, **kwargs):
        data["success"] = False
        super().__init__(data=data, status=status, **kwargs)
