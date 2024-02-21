from tcp import TCPProtocol
from udp import UDPDiscovery
from confgi_handler import ConfigParser

def main():
    config = ConfigParser()
    _, _, _, name = config.read_UDP_config()
    discovery = UDPDiscovery(name)
    discovery.start_discovery()


if __name__ == '__main__':
    main()