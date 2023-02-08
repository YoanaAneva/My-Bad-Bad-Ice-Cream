import socket
import pickle
from threading import Thread, Semaphore
from exchange_info import ExchangeInfo, PlayerInitInfo

# SERVER = "192.168.0.105"
# SERVER = "10.108.5.199"
# SERVER = "10.10.100.210"
SERVER = "192.168.1.4"
PORT = 65432

semaphore = Semaphore() 

players_init_info = [PlayerInitInfo(0 ,0 , "None"), PlayerInitInfo(0, 0, "None")]
exchange_info = [ExchangeInfo("front", (players_init_info[0].player_x, players_init_info[0].player_y, 44, 44), 0, False), 
                 ExchangeInfo("front", (players_init_info[1].player_x, players_init_info[1].player_y, 44, 44), 0, False)]
board = [None]
has_been_updated_by = -1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((SERVER, PORT))
    except socket.error as err:
        print(err)

    s.listen()
    print("Server started, waiting for a connection")

    def initialize_players(conn, player_num):
        players_init_info[player_num] = pickle.loads(conn.recv(2048))

    def communicate_with_client(conn, player_num):
        global has_been_updated_by

        if player_num == 0:
            conn.sendall(pickle.dumps(players_init_info[1]))
        else:
            conn.sendall(pickle.dumps(players_init_info[0]))

        while True:
            data = conn.recv(2048)
            if not data:
                print("Disconnected")
                semaphore.release()
                break
            
            received_info = pickle.loads(data)
            exchange_info[player_num] = received_info

            # updating the server board if a changed board is sent
            if received_info.board:
                semaphore.acquire()
                board[0] = received_info.board
                has_been_updated_by = player_num
                semaphore.release()

            if player_num == 0:
                if has_been_updated_by == 1:
                    has_been_updated_by = -1
                    exchange_info[1].board = board[0]
                conn.sendall(pickle.dumps(exchange_info[1]))
            else:
                if has_been_updated_by == 0:
                    has_been_updated_by = -1
                    exchange_info[0].board = board[0]
                conn.sendall(pickle.dumps(exchange_info[0]))
                
        exchange_info[player_num].has_died = True
        conn.sendall(pickle.dumps(exchange_info[(player_num+1)%2]))

    players = 0
    connections = []
    while True:
        if players >= 2:
            break
        conn, addr = s.accept()
        connections.append(conn)
        print("Connected to:", addr)
        initialize_players(conn, players)
        players += 1

    for i in range(2):
        thread = Thread(target=communicate_with_client, args=[connections[i], i])
        thread.start()


