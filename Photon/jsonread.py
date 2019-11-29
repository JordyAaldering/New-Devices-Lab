import json
import socket
import struct
import time
from urllib.request import urlopen

import cv2
import requests

"""
:param photon_id: The id of the Photon.
:param access_token: The access token of the Photon.
"""
photon_id = "37002a000747333530373233"
access_token = "724392cce6dcd72b7e1c1a9fe063a3b2726d6f6f"


def main():
    """
    Sends the data from the Json page to the Photon.
    """
    url = "http://0.0.0.0:8080/"

    json_url = urlopen(url)
    response = json.loads(json_url.read().decode("utf-8"))

    data = {
        "data": response["data"],
        "access_token": access_token
    }

    response = requests.post("https://api.particle.io/v1/devices/{}/feedback".format(photon_id), data=data)
    print(response)


if __name__ == "__main__":
    time.sleep(1)

    while True:
        main()

        time.sleep(20)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
