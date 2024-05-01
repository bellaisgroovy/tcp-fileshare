import socket
import sys
from utils import RequestType


def receive_put_packet(socket):
    meta_data = socket.recv(516)  # 516 bytes of metadata for all messages (sent to client)

    size = int.from_bytes(meta_data[:40], 'big')
    request_type = determine_request_type(meta_data[40])
    filename = meta_data[41:].decode('utf-8')

    payload = bytes(0)
    data = bytes(1)
    bytes_read = 0
    while bytes_read < size - len(meta_data):
        data = socket.recv(4096)

        payload += data
        bytes_read += len(data)
    packet = {
        'size': size,
        'request_type': request_type,
        'filename': filename,
        'payload': payload
    }

    return packet


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
    # send get request
    path = sys.argv[4]
    request = get_request(path)
    cli_sock.sendall(request)

    # receive put packet
    packet = receive_put_packet(cli_sock)

    # write payload to file
    with open(path, 'wb') as file:
        file.write(packet['payload'])
elif request_type == 'put':
    path = sys.argv[4]
    request = put_request(path)
    cli_sock.sendall(request)
