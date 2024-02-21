import socket
import json
import sys

sys.path.append("..")
from ..confgi_handler import ConfigParser


class TCPProtocol:
    """
    A class for handling TCP communication protocol between peers.
    """

    def __init__(self, peer_id):
        """
        Initializes a new instance of the TCPProtocol class with the specified peer ID.

        Parameters:
            peer_id (str): The unique identifier of the peer.
        """
        #config = ConfigParser()
        #ctcp_port = config.read_TCP_config()
        self.peer_id = peer_id
        self.tcp_port = 9876
        self.tcp_server = None

    def establish_tcp_connection(self, peer_ip):
        """
        Establishes a TCP connection with the specified peer.

        Parameters:
            peer_ip (str): The IP address of the peer to connect to.
        """
        try:
            self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_server.connect((peer_ip, self.tcp_port))
            self.perform_handshake()
        except Exception as e:
            print("Error establishing TCP connection:", str(e))

    def perform_handshake(self):
        """
        Performs handshake with the connected peer over TCP connection.
        """
        try:
            handshake_msg = json.dumps({"command": "hello", "peer_id": self.peer_id})
            handshake_msg += "\n"
            self.tcp_server.sendall(handshake_msg.encode("utf-8"))
            response = self.tcp_server.recv(1024).decode("utf-8")
            self.handle_tcp_response(response)
        except Exception as e:
            print("Error during handshake:", str(e))

    def handle_tcp_response(self, response):
        """
        Handles the response received from the peer during handshake.

        Parameters:
            response (str): The response message received from the peer over TCP connection.
        """
        try:
            response_json = json.loads(response)
            if response_json.get("status") == "ok":
                print("Handshake successful. Received message history:", response_json.get("messages"))
        except json.JSONDecodeError:
            print("Invalid JSON received during handshake:", response)

    def send_message(self, message_id, message):
        """
        Sends a message to the connected peer over TCP connection.

        Parameters:
            message_id (str): The ID of the message.
            message (str): The message content.
        """
        try:
            message_data = {"command": "new_message", "message_id": message_id, "message": message}
            message_json = json.dumps(message_data)
            self.tcp_server.sendall(message_json.encode("utf-8"))
            response = self.tcp_server.recv(1024).decode("utf-8")
            self.handle_message_response(response)
        except Exception as e:
            print("Error sending message:", str(e))

    def handle_message_response(self, response):
        """
        Handles the response received from the peer after sending a message.

        Parameters:
            response (str): The response message received from the peer over TCP connection.
        """
        try:
            response_json = json.loads(response)
            if response_json.get("status") == "ok":
                print("Message sent successfully.")
        except json.JSONDecodeError:
            print("Invalid JSON received after sending message:", response)