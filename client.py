class Client:
    def get(self, filename):
        name_packet = filename.encode() + bytearray(1020-len(filename.encode()))  # fills packet
        payload = self.get_payload(filename)


    def get_payload(self, filename):
        return open(filename, 'rb').read()