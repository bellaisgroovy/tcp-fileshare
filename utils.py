from enum import Enum

zero = 0
one = 1
two = 2


class RequestType(Enum):
    PUT = zero.to_bytes()
    GET = one.to_bytes()
    LIST = two.to_bytes()

    @staticmethod
    def determine_request_type(request_bytes):
        if request_bytes == RequestType.PUT.value:
            return RequestType.PUT
        elif request_bytes == RequestType.GET.value:
            return RequestType.GET
        if request_bytes == RequestType.LIST.value:
            return RequestType.LIST


