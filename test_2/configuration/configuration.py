import configparser

class Configuration:
    def __init__(self):
        self.peer_id = None
        self.broadcast_address = None
        self.port = None

    def read_config(self):
        udp_config = configparser.ConfigParser()
        udp_config.read("../config/config.ini")

        if not self.check_for_invalid_input(udp_config):
            raise ValueError("Please check your config settings")
        return self.peer_id, self.broadcast_address, self.port

    def check_for_invalid_input(self, udp_config):
        try:
            self.peer_id = udp_config.get('NETWORK_INFO', 'peer_id')
            self.broadcast_address = udp_config.get('NETWORK_INFO', 'broadcast_address')
            self.port = int(udp_config.get('NETWORK_INFO', 'port'))
            if not (self.peer_id and self.broadcast_address and self.port):
                return False
            return True
        except (configparser.NoOptionError, ValueError) as e:
            return False