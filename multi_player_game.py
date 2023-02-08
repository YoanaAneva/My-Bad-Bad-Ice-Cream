from game import Game
from client import Client
from exchange_info import ExchangeInfo, PlayerInitInfo

class MultiPlayerGame(Game):
    def __init__(self, levels):
        super().__init__(levels)
        self.other_player = None
        self.client = Client()

    def main(self):
        player_init_info = PlayerInitInfo()