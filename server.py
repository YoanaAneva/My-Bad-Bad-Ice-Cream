import socket
import pickle
from pygame import Rect
from threading import Thread, Semaphore
from exchange_info import ExchangeInfo, PlayerInitInfo

SERVER = "192.168.1.4"
PORT = 5555
TIMEOUT = 120

semaphore = Semaphore()

class Server:
    def __init__(self):
        self.levels_waiting_list = {1 : [],   # store a list of tuples containing player's initialization information and its
                                    2 : [],   # connection(socket.socket) for each level
                                    3 : []}
        self.players_init_info = []
        self.exchange_info = []
        self.boards = []
        self.has_been_updated_by = []
        self.connected = [0]

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((SERVER, PORT))
            except socket.error as err:
                print(err)
        
            s.listen()
            print("Server started, waiting for a connection...")
        
            game_num = 0
            while True:
                for i in range(1, 4):
                    if len(self.levels_waiting_list[i]) == 2:
                        self.thread_clients(game_num, self.levels_waiting_list[i])
                        game_num += 1
                        self.levels_waiting_list[i].clear()
        
                try:
                    s.settimeout(TIMEOUT)
                    conn, addr = s.accept()
                    print("Connected to:", addr)
                except TimeoutError as e:
                    if self.connected[0] == 0:
                        print(e)
                        break
        
                init_info = pickle.loads(conn.recv(2048))
                level = init_info.level
                print(level)
                client_conn_and_init_info = (init_info, conn)
                self.levels_waiting_list[level].append(client_conn_and_init_info)   

    def communicate_with_client(self, conn, player_num, game_num):
        global connected
        if player_num == 0:
            conn.sendall(pickle.dumps(self.players_init_info[game_num][1]))
        else:
            conn.sendall(pickle.dumps(self.players_init_info[game_num][0]))

        while True:
            data = conn.recv(2048)
            if not data:
                print("Disconnected")
                semaphore.acquire()
                self.connected[0] -= 1
                semaphore.release()
                break
                
            received_info = pickle.loads(data)
            self.exchange_info[game_num][player_num] = received_info

            # updating the server board if a changed board is sent
            if received_info.board:
                semaphore.acquire()
                self.boards[game_num] = received_info.board                
                self.has_been_updated_by[game_num] = player_num
                semaphore.release()

            if player_num == 0:
                if self.has_been_updated_by[game_num] == 1:
                    self.has_been_updated_by[game_num] = -1
                    self.exchange_info[game_num][1].board = self.boards[game_num]
                conn.sendall(pickle.dumps(self.exchange_info[game_num][1]))
            else:
                if self.has_been_updated_by[game_num] == 0:
                    self.has_been_updated_by[game_num] = -1
                    self.exchange_info[game_num][0].board = self.boards[game_num]
                conn.sendall(pickle.dumps(self.exchange_info[game_num][0]))
                    
        self.exchange_info[game_num][player_num].has_died = True
        conn.sendall(pickle.dumps(self.exchange_info[game_num][(player_num+1)%2]))

    def thread_clients(self, game_num, init_infos):
        self.connected[0] += 2
        self.players_init_info.append([init_infos[0][0], init_infos[1][0]])

        self.exchange_info.append([ExchangeInfo("front", Rect(self.players_init_info[game_num][0].player_x, self.players_init_info[game_num][1].player_y, 44, 44), 0, False), 
                            ExchangeInfo("front", Rect(self.players_init_info[game_num][0].player_x, self.players_init_info[game_num][1].player_y, 44, 44), 0, False)])
        self.boards.append(None)
        self.has_been_updated_by.append(-1)

        for i in range(2):
            thread = Thread(target=self.communicate_with_client, args=[init_infos[i][1], i, game_num])
            thread.start()


s = Server()
s.start()