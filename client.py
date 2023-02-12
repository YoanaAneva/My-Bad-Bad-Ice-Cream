import socket
import pickle
from exchange_info import ExchangeInfo, PlayerInitInfo

SERVER = "192.168.1.4"
PORT = 5555
TIMEOUT = 40

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (SERVER, PORT)

    def connect_to_server(self, data: PlayerInitInfo):
        try:
            self.client.settimeout(TIMEOUT)
            self.client.connect(self.addr)
        except socket.error as error:
            print(error)
            self.client.close()

        self.client.sendall(pickle.dumps(data))
    
    def get_init_info(self) -> PlayerInitInfo:
        data = self.client.recv(2048)
        return pickle.loads(data)

    def send(self, data) -> ExchangeInfo:
        try:
            self.client.sendall(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as error:
            print(error)
            self.client.close()