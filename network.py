import socket

class Network:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = self.connect()

    def get_connected(self):
        return self.connected

    def connect(self):
        try:
            self.sock.connect((self.ip, self.port))
            print("connection established")
            return True
        except:
            print("connection failed")
            return False

    def send(self, msg):
        self.sock.sendall(str.encode(msg))

    def send_obj(self, obj):
        self.sock.sendall(obj)

    def recv(self, bandwidth):
        return self.sock.recv(bandwidth)