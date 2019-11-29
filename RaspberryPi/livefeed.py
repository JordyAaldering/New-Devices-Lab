import os
import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

import finddeck
import line
from card import deck_to_string


def initialise():
    """
    Initialise the camera and grab a reference to the raw camera capture.
    :return: The camera and raw capture.
    """
    camera = PiCamera()
    camera.resolution = (1920, 1088)
    camera.rotation = 180
    camera.framerate = .5

    raw_capture = PiRGBArray(camera, size=(1920, 1088))

    # Allow the camera to warm up.
    time.sleep(.1)

    return camera, raw_capture


def make_images():
    """
    Creates images of an ordered deck and saves them.
    """
    camera, raw_capture = initialise()

    i = 1
    # Capture frames from the camera.
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array.copy()
        raw_capture.truncate(0)

        finddeck.print_image(image)

        if not os.path.exists("Images_Ordered"):
            os.makedirs("Images_Ordered")

        write_path = "Images_Ordered/{:04d}.png".format(i)
        if not os.path.exists(write_path):
            cv2.imwrite(write_path, frame)

        i += 1

        # Break from the loop if the q key was pressed.
        if cv2.waitKey(1) == ord("q"):
            break


def main(print_info=False, show_image=False):
    """
    Gets frames from the camera and turns them into decks.
    These decks are saved to a file as a string.
    :param print_info: Whether to print the deck info.
    :param show_image: Whether to print the frame and cropped image.
    """
    camera, raw_capture = initialise()

    # Capture frames from the camera.
    for frame in camera.capture_continuous(raw_capture, format='bgr', use_video_port=True):
        image = frame.array.copy()
        raw_capture.truncate(0)

        try:
            corners, _, _, box = finddeck.compute_bounds(image)
        except IndexError:
            continue

        cropped = finddeck.crop_deck(image, box)
        deck = line.get_filtered_deck(cropped)

        with open("jsondata.txt", "w+") as f:
            f.write(deck_to_string(deck))

        if print_info:
            print(", ".join([str(c) for c in deck]))
            print("Accuracy: {:.2f}%".format(line.accuracy_score(deck)))

        if show_image:
            cv2.imshow("Cropped", cropped)
            finddeck.print_image(image, corners=corners, box=box)

        # Break from the loop if the q key was pressed.
        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    try:
        main()
    finally:
        cv2.destroyAllWindows()
