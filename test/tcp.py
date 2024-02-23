import json
import socket
from datetime import datetime

class TCPProtocol:
    def __init__(self, peer_id):
        self.tcp_port = 9876
        self.peer_id = peer_id

    def establish_connectio(self, peer_ip):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((peer_ip, self.tcp_port))
                self.perform_handshake(s)
                print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: TCP chat: TCP connection established with {peer_ip}")
        except Exception as e:
            print("Error establishing TCP connection:", str(e))

    def perform_handshake(self, s):
        try:
            handshake_msg = json.dumps({"command": "hello", "peer_id": self.peer_id})
            handshake_msg += "\n"
            s.sendall(handshake_msg.encode("utf-8"))
            response = s.recv(1024).decode("utf-8")
            self.handle_tcp_response(response)
        except Exception as e:
            print("Error during handshake:", str(e))

    def handle_tcp_response(self, response):
        try:
            response_json = json.loads(response)
            if response_json.get("status") == "ok":
                print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: Handshake successful with {response_json.get('peer_id')}")
        except Exception as e:
            print("Invalid JSON received during handshake:", response)