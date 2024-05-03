import socket as sock_lib
import sys
from common_utilities import *

HOME_DIR = 'client_data'


def main():  # called at bottom of file
    try:
        cli_sock = create_socket()

        request_type = RequestType.determine_request_type_from_string(request_str=sys.argv[3])

        if request_type == RequestType.GET:
            request_get(cli_sock)
        elif request_type == RequestType.PUT:
            request_put(cli_sock)
        elif request_type == RequestType.LIST:
            request_list(cli_sock)
    except Exception as error:
        print(error)
        exit(1)


def create_socket():
    cli_sock = sock_lib.socket(sock_lib.AF_INET, sock_lib.SOCK_STREAM)

    srv_addr = (sys.argv[1], int(sys.argv[2]))

    print(srv_addr, end=' ')

    try:
        cli_sock.connect(srv_addr)
    except sock_lib.gaierror:
        print(f'cant be reached, check hostname is correct')
    except ConnectionRefusedError:
        print(f'refused connection, check port is correct')
        exit(1)

    return cli_sock


# GET request

def request_get(socket):
    filename = sys.argv[4]
    path = filename_to_path(filename, HOME_DIR)

    packet = create_get_request(filename)

    socket.sendall(packet)

    download_file(path, len_size_bytes=40, socket=socket)
    print(f'success downloaded {filename}')


def create_get_request(filename):
    request_type = RequestType.GET.value

    name_packet = pack(len_size_bytes=2, data=filename.encode())

    packet = request_type + name_packet
    return packet


# PUT request

def request_put(socket):
    filename = sys.argv[4]
    path = filename_to_path(filename, HOME_DIR)

    packet = create_put_request(filename, path)

    socket.sendall(packet)
    print(f'success sent {filename}')


def create_put_request(filename, path):
    request_type = RequestType.PUT.value

    name_packet = pack(len_size_bytes=2, data=filename.encode())

    file_packet = get_file_packet(path, len_size_bytes=40)
    packet = request_type + name_packet + file_packet
    return packet

# LIST request

def request_list(socket):
    packet = RequestType.LIST.value
    socket.sendall(packet)
    print("success")
    receive_list(socket)


def receive_list(socket):
    list_bytes = big_recv(len_size_bytes=40, socket=socket)
    list_str = list_bytes.decode('utf-8')
    print(list_str)


main()
