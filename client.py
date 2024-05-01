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


def list_request():
    request_type = RequestType.LIST.value

    size = 40 + len(request_type)
    try:
        size = size.to_bytes(40)
    except OverflowError:
        print('max packet size is ~136GB')

    packet = size + request_type
    return packet


def fill_string_packet(string, max_size_bytes):
    return string.encode() + bytes(max_size_bytes - len(string.encode()))


def get_payload(filename):
    return open(filename, 'rb').read()


# main

cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_addr = (sys.argv[1], int(sys.argv[2]))

try:
    cli_sock.connect(srv_addr)
except socket.gaierror:
    print('cant reach address specified')
    exit(1)

request_type = sys.argv[3]
if request_type == 'list':
    request = list_request()
    cli_sock.sendall(request)
elif request_type == 'get':
    path = sys.argv[4]
    request = get_request(path)
    cli_sock.sendall(request)
elif request_type == 'put':
    path = sys.argv[4]
    request = put_request(path)
    cli_sock.sendall(request)
