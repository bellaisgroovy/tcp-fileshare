import socket as sock_lib
import sys
from common_utilities import *

HOME_DIR = 'client_data'


def main():  # called at bottom of file
    cli_sock = create_socket()

    request_type = RequestType.determine_request_type_from_string(request_str=sys.argv[3])

    if request_type == RequestType.GET:
        request_get(cli_sock)


def create_socket():
    cli_sock = sock_lib.socket(sock_lib.AF_INET, sock_lib.SOCK_STREAM)
    srv_addr = (sys.argv[1], int(sys.argv[2]))

    print(str(srv_addr), end=' ')

    try:
        cli_sock.connect(srv_addr)
    except sock_lib.gaierror:
        print('cant reach address')
        exit(1)
    except ConnectionRefusedError:
        print('server refused connection')
        exit(1)

    return cli_sock


def request_get(socket):
    filename = sys.argv[4]
    path = filename_to_path(filename, HOME_DIR)

    packet = create_get_request(path, filename)

    socket.sendall(packet)

    download_file(path, max_bytes=40, socket=socket)
    print(f'downloaded {filename}')


def create_get_request(path, filename):
    request_type = RequestType.GET.value

    name_packet = create_string_packet(filename, max_bytes=1020)

    packet = request_type + name_packet
    return packet

main()