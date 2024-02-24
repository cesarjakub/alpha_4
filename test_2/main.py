import threading
from udp_tcp import HandleUDPandTCP

def main():
    udp_tcp = HandleUDPandTCP("cesar-peer", "172.31.255.255", 9876)

    udp_thread_one = threading.Thread(target=udp_tcp.udp_discovery)

    try:
        udp_thread_one.daemon = True
        udp_thread_one.start()

        udp_tcp.listen_udp()
    except KeyboardInterrupt:
        udp_thread_one.join()
        print("Something went wrong with Threads")


if __name__ == '__main__':
    main()