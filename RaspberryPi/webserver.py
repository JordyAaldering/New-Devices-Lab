import json

import cv2
import numpy as np
from flask import Flask, request

from line import get_filtered_deck

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    """
    Receive an image through an HTTP request, decode it and respond with the
    cards found in the image.
    :return: HTTP response containing json encoded card codes.
    """
    r = request

    # Convert string of image data to uint8.
    np_arr = np.fromstring(r.data, np.uint8)

    # Decode image
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    deck = get_filtered_deck(image)
    deck_strings = [str(c) for c in deck]

    # Build a response dict to send back to client.
    json_dump = json.dumps({"deck": deck_strings})
    response = app.response_class(response=json_dump, status=200, mimetype="application/json")

    return response
