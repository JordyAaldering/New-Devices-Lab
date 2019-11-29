import os
from itertools import groupby

import cv2

from card import get_card_old, Card

"""
Get codes parameters.
:param width_params: How much to change widths, for error correction.
"""
width_params = [1.17, 1.9, 2.94]


def get_runs(line):
    """
    Gets the runs of a line.
    :param line: One line of the deck image.
    :return: Array of codes extracted from the line image.
    """
    groups = groupby(line)
    groups = [(x, len(list(y))) for x, y in groups]
    groups = [(x, y) for x, y in groups if y > 1]

    if groups[0][0] == 255:
        # First is white.
        groups.pop(0)

    for i in range(len(groups)):
        try:
            while groups[i][0] == groups[i + 1][0]:
                groups[i][1] += groups[i + 1][1] + 1
        except IndexError:
            break

    runs = [y for x, y in groups]
    return runs


def get_start(runs, variance):
    """
    Gets the start of the code in the runs array.
    :param runs: Array of codes.
    :param variance: Variance for error correction.
    :return: The start index of the card code.
    """
    candidates = [runs[i:i + 3] for i in range(0, len(runs) - 2)]

    for index, candidate in enumerate(candidates):
        if (candidate[1] + variance >= candidate[0] >= candidate[1] - variance and
                candidate[2] + variance >= candidate[0] >= candidate[2] - variance):
            return index


def get_unit_width(runs, start):
    """
    Gets the expected width of the codes.
    :param runs: Array of codes.
    :param start: Start index of the card code.
    :return: Expected width of codes.
    """
    return int(round((runs[start] + runs[start + 1] + runs[start + 2]) / 3))


def get_codes(whites, blacks, width):
    """
    Gets the codes from the whites and blacks.
    :param whites: Array containing the white parts of the code, starting in front of the first black.
    :param blacks: Array containing the black parts of the code.
    :param width: Width of code segments.
    :return: The corresponding code.
    """
    codes = []

    for i, black in enumerate(blacks):
        if black < width * width_params[0]:
            if i == 0:
                if whites[0] > width_params[1] * width:
                    # | www www RRR ...
                    codes.append("01")
                else:
                    # | www LLL www  ...
                    codes.append("10")
            else:
                if codes[i - 1] != "10" and whites[i] > width_params[1] * width:
                    # ... www RRR www www RRR ...
                    # ... FFF FFF www www RRR ...
                    codes.append("01")
                elif whites[i] > width_params[2] * width:
                    # ... www www www RRR ...
                    codes.append("01")
                else:
                    # ... LLL www LLL www ...
                    # ... www www LLL www ...
                    codes.append("10")
        else:
            # ... FFF FFF ...
            codes.append("11")

    return codes


def print_info(runs, start, width, whites, blacks, codes, index, line, image):
    """
    Prints info of the deck.
    :param runs: Array of codes.
    :param start: Start index of the card code.
    :param width: Width of code segments.
    :param whites: Array containing the white parts of the code, starting in front of the first black.
    :param blacks: Array containing the black parts of the code.
    :param codes: The codes found in the current line.
    :param index: The index of the found line.
    :param line: The current found line.
    :param image: The image.
    """
    print("Runs:", runs)
    print("Start:", start)
    print("Width:", width)

    print("Whites:", whites)
    print("Blacks:", blacks)

    print("Codes:", " ".join([x.name for x in codes]))
    print("Codes:", " ".join([x.value for x in codes]))

    cv2.imshow("Line", line)
    cv2.imshow("Image", image)
    cv2.line(image, (0, index), (len(line), index), (255, 0, 0), 1)


def get_deck(image, show_image=False):
    """
    Turns an image into a deck.
    :param image: The image.
    :param show_image: Whether to show the image and corresponding info.
    :return: A deck.
    """
    deck = []
    for index, row in enumerate(image):

        try:
            runs = get_runs(row)
            start = get_start(runs, 6)
            width = get_unit_width(runs, start)
        
            whites = [runs[start + i] for i in range(3, 11, 2)]
            blacks = [runs[start + i] for i in range(4, 12, 2)]

            codes = get_codes(whites, blacks, width)
            deck.append(codes)

            if show_image:
                print_info(runs, start, width, whites, blacks, codes, index, row, image)

                key = cv2.waitKey(0)
                if key == ord("q"):
                    cv2.destroyAllWindows()
                    break
        except IndexError:
            pass
        except TypeError:
            pass

    return deck


def lookup_card(code):
    """
    Gets a card from a code.
    :param code: The code of the card.
    :return: The card corresponding to the code.
    """
    try:
        card = get_card_old(code)
        return card
    except LookupError:
        return None


def get_filtered_deck(image):
    """
    Gets an image and turns it into a filtered array of cards.
    :param image: The image to get the deck from.
    :return: A filtered array of cards.
    """
    deck = [lookup_card(card) for card in get_deck(image)]
    deck = [card for card in deck if card is not None]
    groups = groupby(deck, lambda x: (x.rank, x.suit))
    deck = [Card(x[0], x[1]) for x, y in groups if len(list(y)) >= 2]

    return deck


def accuracy_score(deck):
    """
    Gets the accuracy of a found deck with a known order.
    :param deck: A deck with a fixed order.
    :return: The accuracy score a known deck.
    """
    correct = 0
    for suit in range(0, 4):
        for rank in range(0, 13):
            index = suit * 13 + rank
            correct += check_range(deck, index, rank, suit)

    return correct / 52 * 100


def check_range(deck, index, rank, suit):
    """
    Checks whether the requested card is within a certain range.
    :param deck: The deck.
    :param index: The index of the middle card.
    :param rank: The rank of the card to check.
    :param suit: The suit of the card to check.
    :return: True if the middle card or one of its neighbours is equal to Card(rank, suit).
    """
    for i in range(max(0, index - 1), min(index + 2, len(deck))):
        if deck[i] == Card(rank, suit):
            return 1

    return 0


def main():
    """
    Prints the cards of a deck and the corresponding accuracy.
    """
    images = []
    count = 0
    limit = 120

    for path in os.listdir("Images_Ordered_Cropped"):
        if count > limit:
            break

        count += 1
        images.append(cv2.imread("Images_Ordered_Cropped/" + path, 0))

    ms = 0
    best_codes = []
    for image in images:
        deck = get_filtered_deck(image)
        score = accuracy_score(deck)

        if score > ms:
            ms = score
            best_codes = [i for i in deck]

    print(ms, [str(card) for card in best_codes])


if __name__ == "__main__":
    try:
        main()
    finally:
        cv2.destroyAllWindows()
