import socket
import threading
import pickle
from game import *

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = True
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.main_socket.bind((ip, port))
        except:
            print("binding failed")
            quit()
        self.main_socket.listen()
        print("waiting for connection...")
        self.main_server()

    def interaction(self, conn, g, player_id):
        interact = True
        conn.sendall(str.encode(str(player_id)))
        g.change_players_present(player_id)
        conn.sendall(pickle.dumps(g))
        while interact:
            data = conn.recv(2048)
            msg = data.decode('utf-8')
            if not msg:
                g.change_players_terminate(player_id)
                interact = False
            elif msg == 'get':
                conn.sendall(pickle.dumps(g))
            elif msg == 'move':
                player_move = pickle.loads(conn.recv(2048))
                g.make_move(player_id, player_move)
                g.change_turn()
                g.check_winner()
                conn.sendall(pickle.dumps(g))
        conn.close()
        print("connection closed with player = ", player_id)

    def main_server(self):
        gameID = 0
        g = None
        player_count = 0
        thread_details = []
        while self.running:
            print('hello')
            new_socket, client_ip = self.main_socket.accept()
            print("connection established with ip = ", client_ip)
            if player_count == 0:
                g = Game(gameID)
                thread_details.append(threading.Thread(target=self.interaction, args=(new_socket, g, player_count)))
                thread_details[0].start()
                player_count = (player_count + 1) % 2
            elif player_count == 1:
                thread_details.append(threading.Thread(target=self.interaction, args=(new_socket, g, player_count)))
                thread_details[1].start()
                player_count = (player_count + 1) % 2
                gameID += 1
            if gameID == 1:
                self.running = False
        self.main_socket.close()
        print('main socket closed')
        thread_details[0].join()
        thread_details[1].join()