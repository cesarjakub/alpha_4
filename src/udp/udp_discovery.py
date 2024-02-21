import socket
import json
import time
import sys
from datetime import datetime
sys.path.append("..")
from ..tcp import TCPProtocol
from ..confgi_handler import ConfigParser

class UDPDiscovery:
    """
    A class for performing UDP discovery to find peers on the network.
    """
    def __init__(self, peer_id):
        """
        Initializes a new instance of the UDPDiscovery class with the specified peer ID.

        Parameters:
            peer_id (str): The unique identifier of the peer initiating the discovery process.
        """

        #config = ConfigParser()
        #cudp_port, cudp_interval, cudp_broadcast_address, _  = config.read_UDP_config()

        #self.udp_interval = cudp_interval
        #self.udp_broadcast_address = cudp_broadcast_address
        self.peer_id = peer_id
        self.udp_port = 9876
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.peer_addresses = set()

    def send_udp_message(self, message):
        """
        Sends a UDP broadcast message to discover peers on the network.

        Parameters:
            message (str): The message to be sent.
        """
        self.sock.sendto(message.encode("utf-8"), ("172.31.255.255", self.udp_port))

    def receive_udp_message(self):
        """
        Receives a UDP message from the network.

        Returns:
            Tuple (str, tuple): A tuple containing the received message as a string and the address of the sender.
        """
        data, addr = self.sock.recvfrom(1024)
        return data.decode("utf-8"), addr

    def handle_udp_response(self, response):
        """
        Handles the response received from peers.

        Parameters:
            response (str): The response message received from a peer.
        """
        try:
            response_json = json.loads(response)
            if response_json.get("status") == "ok":
                peer_id = response_json["peer_id"]
                status = response_json["status"]
                print(f"Discovered peer: {peer_id}")
                print(f"{datetime.now()} {self.peer_id}: UDPDiscovery: Server: Received request from - status: {status} peer_id: {peer_id}")

        except Exception as e:
            print(f"Error handling UDP response: {e}")

    def start_discovery(self):
        """
        Initiates the UDP discovery process by sending periodic broadcast messages and handling responses.
        """
        while True:
            self.send_udp_message(json.dumps({"command": "hello", "peer_id": self.peer_id}))
            self.sock.settimeout(5)
            while True:
                try:
                    response, addr = self.receive_udp_message()
                    self.handle_udp_response(response)
                    tcp = TCPProtocol(self.peer_id)
                    tcp.establish_tcp_connection(addr[0])
                except socket.timeout:
                    break
            time.sleep(5)