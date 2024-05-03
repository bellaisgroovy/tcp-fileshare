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
    num_bytes = socket.recv(no_bytes)
    num_int = int.from_bytes(num_bytes, 'big')
    return num_int


def get_str_from_socket(no_bytes, socket):
    filename_bytes = socket.recv(no_bytes)
    filename = filename_bytes.decode('utf-8')


def get_filename(socket):
    filename_len = get_int_from_socket(no_bytes=2, socket=socket)
    filename_bytes = socket.recv(filename_len)
    filename = filename_bytes.decode('utf-8')

    return filename


def send_file(socket, path):
    packet = get_file_packet(path, len_size_bytes=40)

    socket.sendall(packet)


def get_file_packet(path, len_size_bytes):
    file_bytes = get_file_bytes(path)
    len_bytes = get_len_bytes(file_bytes, len_size_bytes)
    packet = len_bytes + file_bytes
    return packet


def get_file_bytes(path):
    with open(path, 'rb') as file:
        file_bytes = file.read()

    return file_bytes


def get_len_bytes(data, max_bytes):
    length = len(data)
    len_bytes = length.to_bytes(max_bytes, 'big')
    return len_bytes


def filename_to_path(filename, home_dir):
    return os.path.join(home_dir, filename)


def pack(len_size_bytes, data):
    """
    creates packet of data with preceding length value.
    len_size_bytes = the number of bytes used to represent the length of data.
    data is in bytes.
    """
    len_data_bytes = len(data).to_bytes(len_size_bytes, 'big')  # length of data in bytes
    packet = len_data_bytes + data
    return packet


def download_file(path, len_size_bytes, socket):
    file_bytes = big_recv(len_size_bytes, socket)
    bytes_to_file(path, file_bytes)


def big_recv(len_size_bytes, socket):
    old_time_out = socket.gettimeout()
    socket.settimeout(10)  # if recv takes over 10 seconds it will time out

    size_bytes = int.from_bytes(socket.recv(len_size_bytes), 'big')

    data = bytes(1)
    bytes_read = 0
    big_data = bytes(0)

    while len(data) > 0 and bytes_read < size_bytes:  # while connection is open and full file isn't read
        data = socket.recv(4096)

        big_data += data

        bytes_read += len(data)
    if len(data) == 0:
        raise ConnectionAbortedError(f'Connection was closed by {socket.getsockname()}')

    socket.settimeout(old_time_out)  # reset timeout to normal
    return big_data


def bytes_to_file(path, file_bytes):
    with open(path, 'wb') as file:
        file.write(file_bytes)
