import socket
import sys


def get_request(filename):
    name_packet = fill_string_packet(filename, max_size_bytes=1020)
    payload = get_payload(filename)
    size = len(name_packet) + len(filename)
    try:
        size = size.to_bytes(40)
    except OverflowError:
        print('max packet size is ~136GB')


def fill_string_packet(string, max_size_bytes):
    return string.encode() + bytearray(max_size_bytes - len(string.encode()))


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
