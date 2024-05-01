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


def put_request(filename):
    request_type = RequestType.PUT.value

    name_size_bytes = len(filename).to_bytes(2, 'big')
    name_packet = fill_string_packet(filename, max_size_bytes=1020)

    payload = get_payload(filename)
    payload_size_bytes = len(payload).to_bytes(40, 'big')  # TODO validation

    packet = request_type + name_size_bytes + name_packet + payload_size_bytes + payload
    return packet


def fill_string_packet(string, max_size_bytes):
    return string.encode() + bytes(max_size_bytes - len(string.encode()))


def get_payload(filename):
    return open(filename, 'rb').read()
