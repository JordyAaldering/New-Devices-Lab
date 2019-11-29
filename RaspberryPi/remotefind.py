from glob import glob

import cv2
import requests

import line
from livefeed import initialise


def get_server_answer(image, address):
    """
    ...
    :param image: The image from the camera.
    :return: A json response containing the found codes by the server.
    """
    content_type = "image/jpeg"
    headers = {"content-type": content_type}
    _, encoded = cv2.imencode(".png", image)

    r = requests.post(address, data=encoded.tostring(), headers=headers)

    return r.json()


def main(print_info=False, address="http://145.116.146.92:9002"):
    """
    This function tests the server's response to the PI camera feed. Each frame
    is sent to the server and the response and its accuracy are printed. 
    :param address: The IP address (and port) of the remote server.
    """
    camera, raw_capture = initialise()

    # Capture frames from the camera.
    for frame in camera.capture_continuous(raw_capture, format='bgr', use_video_port=True):
        image = frame.array.copy()
        deck = get_server_answer(image, address)

        print(", ".join([c for c in deck]))
        print("Accuracy: {:.2f}%".format(line.accuracy_score(deck)))

        # Break from the loop if the q key was pressed.
        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    try:
        main()
    finally:
        cv2.destroyAllWindows()
