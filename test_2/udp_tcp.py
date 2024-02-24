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
        self.messages = {}

    # udp handling
    def udp_discovery(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            try:
                while True:
                    message = {"command": "hello", "peer_id": self.peer_id}
                    encoded_message = (json.dumps(message) + "\n").encode("utf-8")
                    udp.sendto(encoded_message, (self.broadcast, self.port))
                    print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: UDPDiscovery: Send message {message}")

                    time.sleep(2)
            except Exception as e:
                print("DISCOVERY Something went wrong")
            finally:
                udp.close()

    def send_udp_response(self, udp):
        while True:
            data, addr = udp.recvfrom(1024)
            res = json.loads(data.decode("utf-8"))
            if res.get("command") == "hello" and res.get("peer_id") != self.peer_id:
                print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: UDPDiscovery: Server: Received request {self.broadcast} from the remote {addr[0]}:{addr[1]} - {res}")

                udp_msg = {"status": "ok", "peer_id": self.peer_id}
                encoded_msg = (json.dumps(udp_msg) + "\n").encode("utf-8")
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_two:
                    udp_two.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    udp_two.connect(addr)
                    udp_two.sendall(encoded_msg)
                    self.tcp_handshake(addr)
                print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: UDPDiscovery: Send response to the remote {addr[0]}:{addr[1]} - {udp_msg}")


    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                udp.bind(('0.0.0.0', self.port))
                self.send_udp_response(udp)
            except Exception as e:
                print("SEND Something went wrong")

    def start_udp(self):
        udp_thread_one = threading.Thread(target=self.udp_discovery)
        udp_thread_two = threading.Thread(target=self.listen)
        try:
            udp_thread_one.start()
            udp_thread_two.start()
        except KeyboardInterrupt:
            udp_thread_one.join()
            udp_thread_two.join()
            print("Something went wrong with Threads")

    # tcp handling
    def tcp_handshake(self, addr):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
            try:
                tcp.connect(addr)
                tcp_msg = {"command": "hello", "peer_id": self.peer_id}
                encoded_msg = (json.dumps(tcp_msg) + "\n").encode("utf-8")
                tcp.sendall(encoded_msg)
                tcp_res = tcp.recv(10000)
                decoded_res = json.loads(tcp_res.decode("utf-8"))
                if decoded_res.get("status") == "ok":
                    print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: TCPProtocol: Handshake established")
                    self.messages.add(decoded_res.get("messages"))
                    print(len(self.messages))
            except Exception as e:
                print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: TCPProtocol: Error during TCP handshake with {addr[0]}:{addr[1]}")

    def handle_tcp_requests(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
            try:
                tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                tcp_server.bind(('0.0.0.0', self.port))
                tcp_server.listen(5)
                while True:
                    conn, addr = tcp_server.accept()
                    threading.Thread(target=self.handle_tcp_client, args=(conn, addr)).start()
            except Exception as e:
                print("TCP Server Something went wrong")

    def handle_tcp_client(self, conn, addr):
        with conn:
            try:
                data = conn.recv(1024)
                if data:
                    received_msg = json.loads(data.decode("utf-8"))
                    if received_msg.get("command") == "hello":
                        print(
                            f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: TCPProtocol: Received handshake request from {addr[0]}:{addr[1]} - {received_msg}")
                        response_msg = {"status": "ok", "messages": self.messages}
                        encoded_response = (json.dumps(response_msg) + "\n").encode("utf-8")
                        conn.sendall(encoded_response)
            except Exception as e:
                print(
                    f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: TCPProtocol: Error handling client {addr[0]}:{addr[1]} - {e}")

    def start_tcp(self):
        tcp_thread = threading.Thread(target=self.handle_tcp_requests)
        try:
            tcp_thread.start()
        except KeyboardInterrupt:
            tcp_thread.join()
            print("Something went wrong with TCP Thread")