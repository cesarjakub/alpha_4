import threading
#from src.configuration.configuration import Configuration
from udp_tcp import HandleUDPandTCP

def main():
    """
    config_info = Configuration()
    try:
        peer_id, broadcast_address, port = config_info.read_config()
        print(peer_id, broadcast_address, port)
    except Exception as e:
        print(e)
        return
    """
    udp_tcp = HandleUDPandTCP("cesar-peer", "172.31.255.255", 9876)
    udp_tcp.start_udp()

if __name__ == '__main__':
    main()