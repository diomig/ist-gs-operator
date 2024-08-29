import socket


class Rotator:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

        self.open_socket()

    def terminate(self):
        self.socket.close()

    def open_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
        except Exception:
            self.connected = False

    def get_position(self):
        self.socket.send("p\x0a".encode())
        return self.socket.recv(20).decode()
