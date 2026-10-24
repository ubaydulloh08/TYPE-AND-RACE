import socket
import threading
import pickle
import time
import random


HOST = '0.0.0.0'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(4)

print("Server is running . Waiting for players")

players = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
is_human = {0: False, 1: False, 2: False, 3: False}
human_count = 0
game_status = "WAITING" 
winner_id = -1
lock = threading.Lock()

FINISH_LINE = 7000

def handle_client(conn, player_id):
    global players, game_status, winner_id
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                break
            
            msg = pickle.loads(data)
            with lock:
                pos = msg["position"]
                cmd = msg["command"]
                
                
                if game_status == "RUNNING":
                    players[player_id] = pos
                    if players[player_id] >= FINISH_LINE:
                        game_status = "FINISHED"
                        winner_id = player_id
                if cmd == "START" and game_status == "WAITING":
                    game_status = "RUNNING"
                elif cmd == "RESTART" and game_status == "FINISHED":
                    for i in range(4):
                        players[i] = 0.0
                    game_status = "WAITING"
                    winner_id = -1
            state_data = {
                "positions": players,
                "status": game_status,
                "winner": winner_id
            }
            conn.sendall(pickle.dumps(state_data))
        except:
            break
            
    print(f"O'yinchi {player_id} uzildi.")
    conn.close()

def accept_connections():
    global human_count
    while human_count < 4:
        conn, addr = server.accept()
        with lock:
            player_id = human_count
            is_human[player_id] = True
            human_count += 1
        
        print(f"REAL PERSON {player_id} ulandi: {addr}")
        conn.send(str(player_id).encode())
        
        thread = threading.Thread(target=handle_client, args=(conn, player_id), daemon=True)
        thread.start()

threading.Thread(target=accept_connections, daemon=True).start()

def main():
    global players, game_status, winner_id
    while True:
        time.sleep(0.1) 
        with lock:
            if game_status == "RUNNING":
                for i in range(4):
                    if not is_human[i]:
                    
                        players[i] += random.uniform(10.0, 30.0)
                        if players[i] >= FINISH_LINE:
                            game_status = "FINISHED"
                            winner_id = i

if __name__ == "__main__":
    main()
