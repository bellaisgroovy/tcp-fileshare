from enum import Enum

zero = 0
one = 1
two = 2


class RequestType(Enum):
    PUT = zero.to_bytes()
    GET = one.to_bytes()
    LIST = two.to_bytes()
