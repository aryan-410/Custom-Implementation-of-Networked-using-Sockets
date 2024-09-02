import socket

class client:
    def __init__(self):
        self.HEADER = 64
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = "192.168.0.187"
        self.ADDR = (self.SERVER, self.PORT)
        self.recieved_message = None

        self.client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connection.connect(self.ADDR)


    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client_connection.send(send_length)
        self.client_connection.send(message)
        self.recieved_message = self.client_connection.recv(2048).decode(self.FORMAT)
