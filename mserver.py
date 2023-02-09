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

# store a list of tuples containing player's initialization information and its
# connection(socket.socket) for each level
levels_waiting_list = {1 : [],
                       2 : [], 
                       3 : []}

players_init_info = []
exchange_info = []

boards = []
has_been_updated_by = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((SERVER, PORT))
    except socket.error as err:
        print(err)

    s.listen()
    print("Server started, waiting for a connection...")

    def communicate_with_client(conn, player_num, game_num):
        if player_num == 0:
            conn.sendall(pickle.dumps(players_init_info[game_num][1]))
        else:
            conn.sendall(pickle.dumps(players_init_info[game_num][0]))

        while True:
            data = conn.recv(2048)
            if not data:
                print("Disconnected")
                semaphore.release()
                break
            
            received_info = pickle.loads(data)
            exchange_info[game_num][player_num] = received_info

            # updating the server board if a changed board is sent
            if received_info.board:
                semaphore.acquire()
                boards[game_num] = received_info.board
                has_been_updated_by[game_num] = player_num
                semaphore.release()

            if player_num == 0:
                if has_been_updated_by[game_num] == 1:
                    has_been_updated_by[game_num] = -1
                    exchange_info[game_num][1].board = boards[game_num]
                conn.sendall(pickle.dumps(exchange_info[game_num][1]))
            else:
                if has_been_updated_by[game_num] == 0:
                    has_been_updated_by[game_num] = -1
                    exchange_info[game_num][0].board = boards[game_num]
                conn.sendall(pickle.dumps(exchange_info[game_num][0]))
                
        exchange_info[game_num][player_num].has_died = True
        conn.sendall(pickle.dumps(exchange_info[game_num][(player_num+1)%2]))

    def thread_clients(game_num, init_infos):
        players_init_info.append([init_infos[0][0], init_infos[1][0]])

        exchange_info.append([ExchangeInfo("front", (players_init_info[game_num][0].player_x, players_init_info[game_num][1].player_y, 44, 44), 0, False), 
                              ExchangeInfo("front", (players_init_info[game_num][0].player_x, players_init_info[game_num][1].player_y, 44, 44), 0, False)])
        boards.append(None)
        has_been_updated_by.append(-1)

        for i in range(2):
            thread = Thread(target=communicate_with_client, args=[init_infos[i][1], i, game_num])
            thread.start()


    game_num = 0

    while True:
        for i in range(1, 4):
            if len(levels_waiting_list[i]) == 2:
                thread_clients(game_num, levels_waiting_list[i])
                game_num += 1
                levels_waiting_list[i].clear()

        conn, addr = s.accept()
        # connections.append(conn)
        print("Connected to:", addr)
        init_info = pickle.loads(conn.recv(2048))
        level = init_info.level
        client_conn_and_init_info = (init_info, conn)
        levels_waiting_list[level].append(client_conn_and_init_info)   

