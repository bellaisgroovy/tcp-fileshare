import os
from enum import Enum

zero = 0
one = 1
two = 2


class RequestType(Enum):
    PUT = zero.to_bytes(1, 'big')
    GET = one.to_bytes(1, 'big')
    LIST = two.to_bytes(1, 'big')

    @staticmethod
    def determine_request_type_from_bytes(request_bytes):
        if request_bytes == RequestType.PUT.value:
            return RequestType.PUT
        elif request_bytes == RequestType.GET.value:
            return RequestType.GET
        if request_bytes == RequestType.LIST.value:
            return RequestType.LIST

    @staticmethod
    def determine_request_type_from_string(request_str):
        if request_str == 'put':
            return RequestType.PUT
        elif request_str == 'get':
            return RequestType.GET
        if request_str == 'list':
            return RequestType.LIST


def get_int_from_socket(no_bytes, socket):
    try:
        num_bytes = socket.recv(no_bytes)
        num_int = int.from_bytes(num_bytes, 'big')
    except Exception as e:
        print('could not convert data to int')
        exit(1)
    return num_int


def get_str_from_socket(no_bytes, socket):
    try:
        filename_bytes = socket.recv(no_bytes)
        filename = filename_bytes.decode('utf-8')
    except Exception as e:
        print('could not convert data to string')
        exit(1)
    return filename


def get_filename(socket):
    filename_len = get_int_from_socket(no_bytes=2, socket=socket)
    filename_bytes = socket.recv(filename_len)
    filename = filename_bytes.decode('utf-8')

    return filename


def send_file(socket, path):
    packet = get_file_packet(path, max_len_bytes=40)

    socket.sendall(packet)


def get_file_packet(path, max_len_bytes):
    file_bytes = get_file_bytes(path)
    len_bytes = get_len_bytes(file_bytes, max_len_bytes)
    packet = len_bytes + file_bytes
    return packet


def get_file_bytes(path):
    try:
        with open(path, 'rb') as file:
            file_bytes = file.read()
    except FileNotFoundError:
        print(f'{path} does not exist.')
        exit(1)

    return file_bytes


def get_len_bytes(data, max_bytes):
    length = len(data)
    len_bytes = length.to_bytes(max_bytes, 'big')
    return len_bytes


def filename_to_path(filename, home_dir):
    return os.path.join(home_dir, filename)


def pack(len_size_bytes, data):
    """
    len_size_bytes = the number of bytes used to represent the length of data.
    data is in bytes.
    """
    len_data_bytes = len(data).to_bytes(len_size_bytes, 'big')  # length of data in bytes
    packet = len_data_bytes + data
    return packet


def create_filled_string_packet(string, max_bytes, max_len_bytes=2):
    try:
        string_bytes = string.encode()
    except Exception:
        print('could not convert string to bytes')
        exit(1)

    try:
        filler = bytes(max_bytes - len(string_bytes))
    except ValueError:
        print('string too long for packet')
        exit(1)

    str_len_bytes = len(string_bytes).to_bytes(max_len_bytes, 'big')

    packet = str_len_bytes + string_bytes + filler
    return packet


def download_file(path, len_max_bytes, socket):
    file_bytes = recv_file_bytes(len_max_bytes, socket)
    bytes_to_file(path, file_bytes)


def recv_file_bytes(max_bytes, socket):
    size_bytes = get_int_from_socket(max_bytes, socket)
    data = bytes(1)
    bytes_read = 0
    file_bytes = bytes(0)

    while len(data) > 0 and bytes_read < size_bytes:  # while connection is open and full file isnt read
        data = socket.recv(4096)

        file_bytes += data

        bytes_read += len(data)

    return file_bytes


def bytes_to_file(path, file_bytes):
    try:
        file = open(path, 'wb')
    except Exception:
        print(f'could not create file at {path}')
        exit(1)

    file.write(file_bytes)
    file.close()
