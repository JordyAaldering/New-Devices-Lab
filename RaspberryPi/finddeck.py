import glob
import os

import cv2
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

import line

"""
Good features parameters.
:param max_corners: Maximum number of corners to find.
:param quality_lvl: Minimal accepted quality of corners.
:param min_distance: Minimum possible Euclidean distance between the corners.
"""
max_corners = 850
quality_lvl = .2
min_distance = 2

"""
Remove outliers parameters.
:param n_neighbors: The actual number of neighbors use for outlier removal.
:param contamination:  The proportion of outliers.
"""
n_neighbors = 30
contamination = "auto"

"""
Improved bounding box parameters. 
:param box_width: The normalized width of the constrained bounding boxes.
"""
box_width = .5

"""
Crop deck parameters.
:param white_threshold: Threshold for distinguishing between black and white pixels.
"""
white_threshold = 62


def good_features(image, print_info=False):
    """
    Determines strong corners on the image to find the markings on the cards.
    :param image: The image to find corners of.
    :param print_info: Whether to print information about this function.
    :return: The found corners.
    """
    gray    = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=max_corners, qualityLevel=quality_lvl, minDistance=min_distance)
    corners = [c[0] for c in corners]
    corners = np.int0(corners)

    if print_info:
        print("Corners:\n", corners)

    return corners


def remove_outliers(coordinates, print_info=False):
    """
    Removes outliers from the coordinates array.
    :param coordinates: The array the remove outliers from.
    :param print_info: Whether to print information about this function.
    :return: The filtered coordinates array.
    """
    clf = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
    y_pred = clf.fit_predict(coordinates)
    coordinates = [coordinates[i] for i in range(len(coordinates)) if y_pred[i] == 1]
    filtered = np.array(coordinates)

    if print_info:
        print("Y pred:\n", y_pred)

    return filtered


def bounding_box_constrained(corners, left_margin, right_margin, print_info=False):
    """
    Creates a bounding box around the corners array within the margins.
    :param corners: corners: The points that have to be contained in the bounding box.
    :param left_margin: A point on the x-axis that specifies the left margin.
    :param right_margin: A point on the x-axis that specifies the right margin.
    :param print_info: Whether to print information about this function.
    :return: The created bounding box around the corners.
    """
    constrained_corners = np.array([c for c in corners if left_margin <= c[0] <= right_margin])
    rect = cv2.minAreaRect(constrained_corners)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    if print_info:
        print("Bounding box constrained from {} to {}:\n{}".format(left_margin, right_margin, box))

    return box


def bounding_box(box_left, box_right, print_info=False):
    """
    Transforms the found constrained bounding boxes into one new bounding box.
    :param box_left: The left constrained bounding box.
    :param box_right: The right constrained bounding box.
    :param print_info: Whether to print information about this function.
    :return: The new bounding box around the whole deck.
    """
    top_left, bottom_left, _, _ = corner_order(box_left)
    _, _, top_right, bottom_right = corner_order(box_right)

    box = np.array([top_left, bottom_left, top_right, bottom_right])

    if print_info:
        print("Improved bounding box:\n", box)

    return box


def corner_order(corners, print_info=False):
    """
    Determine in which order the corners occur.
    :param corners: The points to check.
    :param print_info: Whether to print information about this function.
    :return: The order in which the points occur.
    """
    avg_x = np.mean([x for [x, _] in corners])
    left = [[x, y] for [x, y] in corners if x < avg_x]
    right = [[x, y] for [x, y] in corners if x >= avg_x]

    if left[0][1] > left[1][1]:
        top_left = left[0]
        bottom_left = left[1]
    else:
        top_left = left[1]
        bottom_left = left[0]

    if right[0][1] < right[1][1]:
        top_right = right[0]
        bottom_right = right[1]
    else:
        top_right = right[1]
        bottom_right = right[0]

    if print_info:
        print("Top left: {}, top right: {}, bottom left: {}, bottom right: {}"
              .format(top_left, top_right, bottom_left, bottom_right))

    return top_left, bottom_left, top_right, bottom_right


def crop_deck(image, corners, print_info=False):
    """
    Crops the image according to the corners found earlier.
    The image is cropped such that all corners are still present in the image.
    :param image: The image to crop.
    :param corners: The points that have to be contained in the cropped image.
    :param print_info: Whether to print information about this function.
    :return: The cropped image.
    """
    # Determine in which order the corners occur.
    top_left, bottom_left, top_right, bottom_right = corner_order(corners)

    # Transform the points.
    pts1 = np.float32([bottom_left, top_right, top_left, bottom_right])
    pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])

    m = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(image, m, (300, 300))
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    _, dst = cv2.threshold(dst, white_threshold, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    if print_info:
        print("PTS 1:\n", pts1)
        print("PTS 2:\n", pts2)

    return dst


def compute_bounds(image):
    """
    Computes the features of the specified image
    :param image: The image to compute the features of
    :return: The computed features of the corresponding image
    """
    # Find the markings on the cards and remove outliers.
    resize_factor = 0.5
    image = cv2.resize(image, (0, 0), fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_AREA)
    corners = good_features(image)
    corners = remove_outliers(corners)

    # Find bounding boxes on the left and right parts of the card deck.
    box_begin = min(corners[:, 0])
    box_end = max(corners[:, 0])
    offset = (box_end - box_begin) * box_width

    box_left = bounding_box_constrained(corners, box_begin, box_begin + offset)
    box_right = bounding_box_constrained(corners, box_end - offset, box_end)

    # Transforms the constrained bounding boxes into a big bounding box.
    box = bounding_box(box_left, box_right)
    box_left = box_left * int(1 / resize_factor)
    box_right = box_right * int(1 / resize_factor)
    corners = corners * int(1 / resize_factor)
    box = box * int(1 / resize_factor)

    return corners, box_left, box_right, box


def save_to_file(name, cropped):
    """
    Saves the cropped image to a file if it does not exist yet.
    :param name: The image name.
    :param cropped: The cropped image.
    """
    cv2.imshow("Cropped", cropped)
    if not os.path.exists("Images_Ordered_Cropped"):
        os.makedirs("Images_Ordered_Cropped")

    write_path = "Images_Ordered_Cropped/{}".format(name)
    if not os.path.exists(write_path):
        cv2.imwrite(write_path, cropped)


def print_image(image, corners=None, box_left=None, box_right=None, box=None):
    """
    Prints the image to the screen with the computed features.
    :param image: The original image.
    :param corners: The found markings on the cards.
    :param box_left: The rectangle surrounding markings on the left.
    :param box_right: The rectangle surrounding markings on the right.
    :param box: The improved bounding box using the constrained boxes.
    """
    if corners is not None:
        for i in corners:
            x, y = i.ravel()
            image[y][x] = (0, 0, 255)

    if box_left is not None:
        cv2.drawContours(image, [box_left], 0, (0, 255, 255), 2)

    if box_right is not None:
        cv2.drawContours(image, [box_right], 0, (0, 255, 255), 2)

    if box is not None:
        cv2.drawContours(image, [box], 0, (255, 255, 0), 2)

    cv2.imshow("Image", image)


def main(export_dots=False):
    files = glob.glob("Images_Ordered/*.png")
    acc_scores = []

    for filename in files:
        image = cv2.imread(filename)
        print(filename)

        name = filename.lstrip("Images_Ordered/")
        corners, box_left, box_right, box = compute_bounds(image)

        if export_dots and corners is not None:
            dot_image = np.zeros(image.shape).astype(np.uint8)

            for corner in corners:
                x, y = corner.ravel()
                dot_image[y][x] = (255, 255, 255)
                dot_image_crop = crop_deck(dot_image, box)

                if not os.path.exists("Images_Dots"):
                    os.makedirs("Images_Dots")

                write_path = "Images_Dots/{}".format(name)
                if not os.path.exists(write_path):
                    cv2.imwrite(write_path, dot_image_crop)

        cropped = crop_deck(image, box)
        deck = line.get_filtered_deck(cropped)
        
        save_to_file(name, cropped)
        print_image(image, corners=corners, box_left=box_left, box_right=box_right, box=box)

        score = line.accuracy_score(deck)
        acc_scores.append(score)
        
        print(", ".join([str(c) for c in deck]))
        print("Accuracy: {:.2f}%".format(score))

        # Wait for input until continuing, break from the loop if the q key was pressed.
        key = cv2.waitKey(0)
        if key == ord("q"):
            break

    avg_scores = sum(acc_scores) / len(acc_scores)
    print("Average score:", avg_scores)


if __name__ == "__main__":
    try:
        main()
    finally:
        cv2.destroyAllWindows()
