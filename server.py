import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = {}
picks = {}

player_one = "Waiting..."
player_two = "Waiting..."

message_sent = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients[str(threading.activeCount() - 1)] = addr

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE: connected = False

            if msg != "check" and msg != DISCONNECT_MESSAGE:
                for client, address in clients.items():
                    if address == addr: picks[client] = msg
            
            if msg != "check": print(f"[{addr}] says {msg}")
            if msg == DISCONNECT_MESSAGE:
                print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

            if len(picks) == 2: conn.sendall(f"{picks['1']},{picks['2']}".encode(FORMAT))
            if len(picks) == 1: conn.sendall(str(list(picks.items())[0][1]).encode(FORMAT))
            
            if len(picks) == 0: conn.sendall("Message Recieved !".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] Server is starting...")
start()
