import socket
import pickle
from exchange_info import ExchangeInfo, PlayerInitInfo

SERVER = "192.168.1.4"
PORT = 5555
TIMEOUT = 40

class Client:
    """Class that implemets the logic for a client to server.
    Helps in sending and receiving info from the server.
    """
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (SERVER, PORT)

    def connect_to_server(self, data: PlayerInitInfo):
        """ Connect to the server and send its client
        init info to the server
        """
        try:
            self.client.settimeout(TIMEOUT)
            self.client.connect(self.addr)
        except socket.error as error:
            print(error)
            self.client.close()

        self.client.sendall(pickle.dumps(data))
    
    def get_init_info(self) -> PlayerInitInfo:
        """ Receive the other client init info from the server"""
        data = self.client.recv(2048)
        return pickle.loads(data)


    def send(self, data) -> ExchangeInfo:
        """Send client information and receive 
        the other client info from the server
        """
        try:
            self.client.sendall(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as error:
            print(error)
            self.client.close()
