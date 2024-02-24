import json
import socket
import time
from datetime import datetime
import threading


class HandleUDPandTCP:
    def __init__(self, peer_id, broadcast, port):
        self.peer_id = peer_id
        self.broadcast = broadcast
        self.port = port
        self.lock = threading.Lock()

    def udp_discovery(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            try:
                while True:
                    message = {"command": "hello", "peer_id": self.peer_id}
                    encoded_message = (json.dumps(message) + "\n").encode("utf-8")
                    udp.sendto(encoded_message, (self.broadcast, self.port))
                    print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: UDPDiscovery: Send message {message}")

                    time.sleep(5)
            except Exception as e:
                print("DISCOVERY Something went wrong")
            finally:
                udp.close()

    def send_udp_response(self, data, addr):
        with self.lock:
            try:
                res = json.loads(data.decode("utf-8"))
                if res.get("command") == "hello" and res.get("peer_id") != self.peer_id:
                    print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: UDPDiscovery: Server: Received request {self.broadcast} from the remote {addr[0]}:{addr[1]} - {res}")

                    udp_msg = {"status": "ok", "peer_id": self.peer_id}
                    encoded_response = (json.dumps(udp_msg) + "\n").encode("utf-8")
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as udp:
                        udp.connect((addr[0], self.port))
                        udp.sendall(encoded_response)
                        #tcp handshake
                    print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: UDPDiscovery: Send response to the remote {addr[0]}:{addr[1]} - {udp_msg}")
            except Exception as e:
                print("SEND Something went wrong")

    def listen_udp(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            udp.bind(('0.0.0.0', self.port))
            while True:
                data, addr = udp.recvfrom(1024)
                threading.Thread(target=self.send_udp_response, args=(data, addr)).start()

