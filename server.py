import os
import socket as sock_lib
import sys
from common_utilities import *

HOME_DIR = 'server_data'


def main():  # called at bottom of file
    try:
        port = get_port()
        srv_sock = create_socket(port=port)
    except Exception as e:
        print(e)
        exit(1)

    while True:  # run until error
        try:
            cli_sock, cli_addr = srv_sock.accept()

            print(cli_addr, end=' ')

            request_type = get_request_type(cli_sock)

            if request_type == RequestType.GET:
                serve_get(cli_sock)
            elif request_type == RequestType.PUT:
                serve_put(cli_sock)
                cli_sock.sendall(ErrorCode.SUCCESS.value)  # other requests don't require confirmation
            elif request_type == RequestType.LIST:
                serve_list(cli_sock)

            print('success')  # only reached if no errors
        except FileExistsError as error:
            print(error)
            cli_sock.sendall(ErrorCode.OVERWRITE.value)
        except Exception as error:  # don't exit on errors, other requests will still work
            print(error)
            cli_sock.sendall(ErrorCode.FAILURE.value)


def create_socket(port):
    srv_sock = sock_lib.socket(sock_lib.AF_INET, sock_lib.SOCK_STREAM)
    srv_sock.bind(("0.0.0.0", port))
    srv_sock.listen(5)

    print("server up and running")

    return srv_sock


def get_port():
    try:
        port = int(sys.argv[1])
    except IndexError:
        raise IndexError('a port number must be supplied')
    except ValueError:
        raise ValueError('port must be a number')
    return port


def get_request_type(socket):
    request_bytes = socket.recv(1)

    request_type = RequestType.determine_request_type_from_bytes(request_bytes)
    return request_type


def serve_get(socket):
    print('get', end=' ')
    filename = get_filename(socket)
    path = filename_to_path(filename, HOME_DIR)
    send_file(socket, path)


def serve_put(socket):
    print('put', end=' ')
    filename = get_filename(socket)
    path = filename_to_path(filename, HOME_DIR)
    download_file(path, len_size_bytes=40, socket=socket)


def serve_list(socket):
    print('list', end=' ')

    packet = get_dir_list_packet()

    socket.sendall(packet)


def get_dir_list_packet():
    dir_list_bytes = get_dir_list_bytes()

    len_bytes = len(dir_list_bytes).to_bytes(40, 'big')

    packet = len_bytes + dir_list_bytes

    return packet


def get_dir_list_bytes():
    dir_list = os.listdir(HOME_DIR)
    dir_list_str = ''

    for file in dir_list:
        dir_list_str += file + '\n'

    dir_list_bytes = dir_list_str.encode()

    return dir_list_bytes


main()
