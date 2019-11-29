import socket
import struct

from bottle import *

import card


@get("/")
def serve_json():
    """
    Hosts a Json web page.
    :return: The data to be presented on the web page.
    """
    with open("jsondata.txt", "r") as f:
        data = f.read()

        return {
            "data": data,
            "cards": [str(card.number_to_card(int(str(data[i]) + str(data[i + 1]))))
                      for i in range(0, len(data) - 1, 2)]
        }


def get_ip_address(if_name):
    """
    Gets the ip address of this Raspberry Pi.
    :param if_name: The name to get the ip from.
    :return: The ip address.
    """
    import fcntl
    global sock

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    return socket.inet_ntoa(fcntl.ioctl(
        sock.fileno(),
        0x8915,
        struct.pack("256s", if_name[:15])
    )[20:24])


def main():
    """
    Hosts a Json web page.
    """
    try:
        print(get_ip_address("eth0"))
        run(host="0.0.0.0", port=8080)
    finally:
        sock.close()


if __name__ == "__main__":
    main()
