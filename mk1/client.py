import socket
import sys
from mk1.utils import RequestType, put_request, fill_string_packet
import os


def receive_put_packet(socket):
    request_type = socket.recv(1)  # TODO error handling

    filename_len = int.from_bytes(cli_sock.recv(2), byteorder='big')
    print(filename_len)
    filename = cli_sock.recv(filename_len).decode('utf-8')
    cli_sock.recv(1020 - filename_len)  # empty bits

    payload_size_bytes = int.from_bytes(cli_sock.recv(5), 'big')
    payload = bytes(0)
    data = bytes(1)
    bytes_read = 0
    while len(data) != 0 and bytes_read < payload_size_bytes:
        data = socket.recv(4096)

        payload += data
        bytes_read += len(data)



    return packet


def determine_request_type(request_bytes):
    if request_bytes == RequestType.PUT.value:
        return RequestType.PUT
    elif request_bytes == RequestType.GET.value:
        return RequestType.GET
    if request_bytes == RequestType.LIST.value:
        return RequestType.LIST


def get_request(filename):
    request_type = RequestType.GET.value

    name_packet = fill_string_packet(filename, max_size_bytes=1020)

    size = 40 + len(request_type) + len(name_packet)
    try:
        size = size.to_bytes(40, 'big')
    except OverflowError:
        print('max packet size is ~136GB')

    packet = request_type + name_packet
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


# main

cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_addr = (sys.argv[1], int(sys.argv[2]))

try:
    cli_sock.connect(srv_addr)
    print('connected')
except socket.gaierror:
    print('cant reach address specified')
    exit(1)

request_type = sys.argv[3]

if request_type == 'list':
    request = list_request()
    cli_sock.sendall(request)

elif request_type == 'get':
    print('get start')
    # send get request
    path = sys.argv[4]
    request = get_request(path)
    cli_sock.sendall(request)
    print('get sent')

    # receive put packet
    packet = receive_put_packet(cli_sock)
    print('packet received')

    # write payload to file
    with open(os.path.join('../client_data', path), 'wb') as file:
        file.write(packet['payload'])
    print('written')

elif request_type == 'put':
    path = sys.argv[4]
    request = put_request(path)
    cli_sock.sendall(request)
