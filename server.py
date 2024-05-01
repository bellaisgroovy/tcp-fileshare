import socket
import sys
from utils import RequestType

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_sock.bind(("0.0.0.0", int(sys.argv[1])))  # TODO error handling
srv_sock.listen(5)

while True:
    cli_sock, cli_addr = srv_sock.accept()
    request_type = RequestType.determine_request_type(cli_sock.recv(1))
    if request_type == RequestType.GET:
        # get filename
        filename_len = int.from_bytes(cli_sock.recv(2), byteorder='big')
        filename = cli_sock.recv(filename_len).decode('utf-8')
        cli_sock.recv(1020-filename_len)  # empty bits

        # return put request

