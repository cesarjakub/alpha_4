import configparser

class ConfigParser:
    def __init__(self) -> None:
        pass

    def read_UDP_config(self):
        udp_config = configparser.ConfigParser()
        udp_config.read("config/config.ini")

        udp_port = udp_config.getint('UDP', 'port')
        udp_interval = udp_config.getint('UDP', 'interval')
        udp_broadcast_address = udp_config.get('UDP', 'broadcast_address')
        udp_peer_id = udp_config.get('UDP', 'peer_id')

        return udp_port, udp_interval, udp_broadcast_address, udp_peer_id

    def read_TCP_config(self):
        tcp_config = configparser.ConfigParser()
        tcp_config.read("config/config.ini")

        tcp_port = tcp_config.getint('TCP', 'port')

        return tcp_port