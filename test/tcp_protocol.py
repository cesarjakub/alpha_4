import socket
import threading
from datetime import datetime
import json

# Nastavení
PEER_ID = "your_peer_id"  # Nahraďte vaším ID
BROADCAST_IP = "172.16.0.255"
BROADCAST_PORT = 9876
TCP_PORT = 9877
HISTORY_SIZE = 100  # Počet uchovávaných zpráv

# Seznamy peerů a zpráv
peers = {}  # Klíč: ID klienta, Hodnota: Adresa klienta
messages = {}  # Klíč: ID zprávy (timestamp), Hodnota: Text zprávy

# Vytvoření socketu
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind(('', TCP_PORT))

# Vlákno pro TCP server
def tcp_server_thread():
    while True:
        tcp_socket.listen()
        client, addr = tcp_socket.accept()
        print(f"Nové připojení od {addr[0]}:{addr[1]}")
        handle_tcp_client(client)

# Zpracování TCP klienta
def handle_tcp_client(client):
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break
            request = json.loads(data)

            if request["command"] == "hello":
                send_hello_response(client)
                send_messages(client)

            elif request["command"] == "new_message":
                message_id = request["message_id"]
                message_text = request["message"]
                messages[message_id] = message_text
                send_message_to_all_peers(message_id, message_text)

            else:
                print(f"Neznámý příkaz: {request['command']}")

        except Exception as e:
            print(f"Chyba při komunikaci s klientem: {e}")
            break

    client.close()

# Pomocné funkce
def send_hello_response(client):
    response = {"status": "ok"}
    encoded_response = json.dumps(response).encode()
    client.sendall(encoded_response)

def send_messages(client):
    for message_id, message_text in messages.items():
        response = {"command": "new_message", "message_id": message_id, "message": message_text}
        encoded_response = json.dumps(response).encode()
        client.sendall(encoded_response)

def send_message_to_all_peers(message_id, message_text):
    for peer_id, addr in peers.items():
        if peer_id == PEER_ID:
            continue

        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_client.connect(addr)
            message_json = json.dumps({"command": "new_message", "message_id": message_id, "message": message_text}).encode()
            tcp_client.sendall(message_json)
            response = tcp_client.recv(1024).decode()
            if json.loads(response)["status"] != "ok":
                print(f"Chyba při odesílání zprávy peeru {peer_id}")
        except Exception as e:
            print(f"Chyba při odesílání zprávy peeru {peer_id}: {e}")
        finally:
            tcp_client.close()

# Spuštění serveru
tcp_server_thread = threading.Thread(target=tcp_server_thread)
tcp_server_thread.start()

# Zpracování příkazů
while True:
    command = input("Zadejte příkaz: ")
    if command == "quit":
        break
    elif command.startswith("send "):
        message_text = command[5:]
        message_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        messages[message_id] = message_text
        send_message_to_all_peers()
