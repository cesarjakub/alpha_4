import socket
import time
import json
from datetime import datetime
from threading import Thread

class UDPDiscovery:
    def __init__(self, peer_id, broadcast_ip, broadcast_port):
        self.peer_id = peer_id
        self.broadcast_ip = broadcast_ip
        self.broadcast_port = broadcast_port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.running = False

    def start(self):
        self.running = True
        discovery_thread = Thread(target=self._run_discovery)
        discovery_thread.start()

    def stop(self):
        self.running = False
        self.socket.close()

    def _run_discovery(self):
        while self.running:
            message = {"command": "hello", "peer_id": self.peer_id}
            encoded_message = json.dumps(message).encode("utf-8")
            self.socket.sendto(encoded_message, (self.broadcast_ip, self.broadcast_port))
            self.socket.settimeout(5)

            while True:
                try:
                    data, addr = self.socket.recvfrom(1024)
                    response = json.loads(data.decode("utf-8"))

                    if response.get("command") == "hello":
                        my_response = {"status": "ok", "peer_id": self.peer_id}
                        encoded_response = json.dumps(my_response).encode("utf-8")
                        self.socket.sendto(encoded_response, addr)
                        print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: Server: Sent response to the remote {addr[0]}:{addr[1]} - {my_response}")

                    if response.get("status") == "ok" and response.get("peer_id") != self.peer_id:
                        print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: UDPDiscovery: Server: Received request {self.broadcast_ip} from the remote {addr[0]}:{addr[1]} - {response}")
                except socket.timeout:
                    break

        time.sleep(5)


peer_id = "cesar-peer1"
broadcast_ip = "172.31.255.255"
broadcast_port = 9876

discovery = UDPDiscovery(peer_id, broadcast_ip, broadcast_port)
discovery.start()

