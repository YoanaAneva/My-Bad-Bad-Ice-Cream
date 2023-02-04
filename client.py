import socket
import pickle

SERVER = "192.168.0.103"
PORT = 65432

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (SERVER, PORT)
        # self.info = self.connect_to_server()

    def get_info(self):
        return self.info

    def connect_to_server(self, data):
        try:
            self.client.connect(self.addr)
        except socket.error as error:
            print(error)
            self.client.close()

        self.client.sendall(pickle.dumps(data))
    
    def get_init_info(self):
        data = self.client.recv(2048)
        return pickle.loads(data)

    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as error:
            print(error)
            self.client.close()