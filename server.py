import socket
import pickle
from threading import Thread
from exchange_info import ExchangeInfo, PlayerInitInfo, Info

SERVER = "192.168.0.103"
PORT = 65432

players_init_info = [None, None]
exchange_info = [None, None]
board = None

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
        if player_num == 0:
            conn.sendall(pickle.dumps(players_init_info[1]))
        else:
            conn.sendall(pickle.dumps(players_init_info[0]))

        while True:
            data = conn.recv(2048)
            if not data:
                print("Disconnected")
                break
            
            send_info = pickle.loads(data)
            board = send_info.board
            exchange_info[player_num] = send_info
            print(exchange_info)

            if player_num == 0:
                exchange_info[1].board = board
                conn.sendall(pickle.dumps(exchange_info[1]))
            else:
                exchange_info[0].board = board
                conn.sendall(pickle.dumps(exchange_info[0]))

    players = 0
    connections = []
    while True:
        if players >= 2:
            break
        conn, addr = s.accept()
        connections.append(conn)
        print("Connected to:", addr)
        initialize_players(conn, players)
        print(players)
        players += 1

    for i in range(2):
        thread = Thread(target=communicate_with_client, args=[connections[i], i])
        thread.start()


