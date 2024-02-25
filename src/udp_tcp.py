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

    def udp_response(self, udp):
        while True:
            data, addr = udp.recvfrom(1024)
            res = json.loads(data.decode("utf-8"))
            if res.get("command") == "hello" and res.get("peer_id") != self.peer_id:
                print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: UDPDiscovery: Server: Received request {self.broadcast} from the remote {addr[0]}:{addr[1]} - {res}")
                udp_two = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_two.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                udp_two.connect(addr)
                udp_msg = {"status": "ok", "peer_id": self.peer_id}
                encoded_msg = (json.dumps(udp_msg) + "\n").encode("utf-8")
                udp_two.sendall(encoded_msg)
                self.tcp_handshake(addr)
                print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: UDPDiscovery: Send response to the remote {addr[0]}:{addr[1]} - {udp_msg}")


    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                udp.bind(('0.0.0.0', self.port))
                self.udp_response(udp)
            except Exception as e:
                print("Listen Something went wrong")

    def start_udp(self):
        udp_thread_one = threading.Thread(target=self.udp_discovery)
        udp_thread_two = threading.Thread(target=self.listen)
        try:
            udp_thread_one.start()
            udp_thread_two.start()
            udp_thread_one.join()
            udp_thread_two.join()
        except KeyboardInterrupt:
            print("Something went wrong with Threads")

    # tcp handling
    def tcp_handshake(self, addr):
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.settimeout(3)
            tcp.connect(addr)

            handshake_msg = {"command": "hello", "peer_id": self.peer_id}
            encoded_handshake_msg = (json.dumps(handshake_msg) + "\n").encode("utf-8")
            tcp.sendall(encoded_handshake_msg)

            tcp_res = tcp.recv(100000)
            decoded_res = json.loads(tcp_res.decode("utf-8"))

            if decoded_res.get("status") == "ok":
                print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: TCPProtocol: Handshake established with {addr[0]}:{addr[1]}")
                print(f"Received messages history: {decoded_res.get('messages')}")
            else:
                print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: TCPProtocol: Unexpected response during handshake with {addr[0]}:{addr[1]}")

        except ConnectionRefusedError:
            print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: TCPProtocol: Connection refused by {addr[0]}:{addr[1]}")
        except TimeoutError:
            print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: TCPProtocol: Handshake timed out with {addr[0]}:{addr[1]}")
        except Exception as e:
            print(f"{datetime.now().strftime('%b %d %H:%M:%S')} {self.peer_id}: TCPProtocol: Error during TCP handshake with {addr[0]}:{addr[1]}")
        finally:
            tcp.close()

