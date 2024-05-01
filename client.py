import socket
import sys
from utils import RequestType


def put_request(filename):
    request_type = RequestType.PUT.value

    name_packet = fill_string_packet(filename, max_size_bytes=1020)

    payload = get_payload(filename)

    size = 40 + len(request_type) + len(name_packet) + len(payload)
    try:
        size = size.to_bytes(40)
    except OverflowError:
        print('max packet size is ~136GB')

    packet = size + request_type + name_packet + payload
    return packet


def get_request(filename):
    request_type = RequestType.GET.value

    name_packet = fill_string_packet(filename, max_size_bytes=1020)

    size = 40 + len(request_type) + len(name_packet)
    try:
        size = size.to_bytes(40)
    except OverflowError:
        print('max packet size is ~136GB')

    packet = size + request_type + name_packet
    return packet


def fill_string_packet(string, max_size_bytes):
    return string.encode() + bytes(max_size_bytes - len(string.encode()))


def get_payload(filename):
    return open(filename, 'rb').read()


cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The server's address is a tuple, comprising the server's IP address or hostname, and port number
srv_addr = (sys.argv[1], int(sys.argv[2]))

try:
    cli_sock.connect(srv_addr)
except socket.gaierror:
    print('cant reach address specified')
    exit(1)
