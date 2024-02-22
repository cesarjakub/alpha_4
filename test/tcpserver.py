import socket
import threading
import json
from datetime import datetime

class Peer:
    def __init__(self, peer_id, host, port):
        self.peer_id = peer_id
        self.host = host
        self.port = port
        self.messages = {}

    def send_message(self, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_message(self, conn, addr):
        try:
            with conn:
                data = conn.recv(1024)
                if data:
                    message = json.loads(data.decode())
                    self.process_message(message)
        except Exception as e:
            print(f"Error receiving message: {e}")

    def process_message(self, message):
        command = message.get("command")
        if command == "hello":
            self.send_history()
        elif command == "new_message":
            self.save_message(message)

    def save_message(self, message):
        message_id = message["message_id"]
        if message_id not in self.messages:
            self.messages[message_id] = message

    def send_history(self):
        response = {
            "status": "ok",
            "messages": self.messages
        }
        self.send_message(json.dumps(response))

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Listening for connections on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.receive_message, args=(conn, addr)).start()

if __name__ == "__main__":
    # Create a peer instance
    peer = Peer(peer_id="cesar-peer1", host="localhost", port=9876)
    # Start the server in a separate thread
    threading.Thread(target=peer.start_server).start()
