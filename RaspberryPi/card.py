import warnings

import math

from code import Code


class Card:
    ranks = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
    suits = ["hearts", "spades", "diamonds", "clubs"]

    def __init__(self, rank, suit):
        """
        Initialises this card.
        :param rank: The rank index in the ranks array.
        :param suit: The suit index in the suits array.
        """
        assert 0 <= rank < len(self.ranks), "Rank index out of range."
        assert 0 <= suit < len(self.suits), "Suit index out of range."

        self.rank = rank
        self.suit = suit

    def __lt__(self, other):
        """
        Checks if this card is lower than another card.
        :param other: The card to compare this card to.
        :return: True if this rank is lower or this rank is the same and this suit is lower.
        """
        if self.rank == other.rank:
            return self.suit < other.suit
        elif self.rank == 0:
            return other.rank != 0
        else:
            return self.rank < other.rank

    def __eq__(self, other):
        """
        Checks if this card is equal to another card.
        :param other: The card to compare this card to.
        :return: True if both the rank and the suit are the same.
        """
        return self.rank == other.rank and self.suit == other.suit

    def __str__(self):
        """
        Turns this card into a string.
        :return: This card as a string.
        """
        return "{} of {}".format(self.ranks[self.rank], self.suits[self.suit])


def deck_to_string(deck):
    """
    Turns a deck into a single bitstring of the form xx (repeating),
    where xx is the card represented as a number with a leading zero if necessary.
    :param deck: The deck.
    :return: A bitstring representing the deck.
    """
    return "".join(["{:02d}".format(card.suit * 13 + card.rank) for card in deck])


def string_to_deck(s):
    """
    Turns a bit string into a deck.
    :param s: A string of the form xx (repeating) where xx is an integer representation of a card.
    :return: A deck of cards.
    """
    return [number_to_card(int(s[i] + s[i + 1])) for i in range(0, len(s) - 1, 2)]


def number_to_card(number):
    """
    Turns a number into a card.
    :param number: A number between 0 and 52 (excluding).
    :return: The card corresponding to the number.
    """
    assert 0 <= number < 52, "Card number out of range."
    return Card(number % 13, int(math.floor((number - (number % 13)) / 13)))


def get_card(code):
    """
    Gets the card that corresponds to a certain code.
    :param code: An enum array of codes.
    :return: The card corresponding to the code.
    """
    bitstring = " ".join([c for c in code])

    for suit in range(4):
        for rank in range(13):
            if bitstring == str(Code.from_card(rank, suit)):
                return Card(rank, suit)


def get_card_old(code):
    """
    Gets the card that corresponds to a certain previous version code.
    :param code: An enum array of previous version codes.
    :return: The card corresponding to the previous version code.
    """
    warnings.warn("Deprecated, use get_card instead with the new codes.", DeprecationWarning)

    bitstring = " ".join([c for c in code])

    if bitstring == "01 01 01 01": return Card(0, 0)
    if bitstring == "11 01 01 01": return Card(1, 0)
    if bitstring == "01 11 01 01": return Card(2, 0)
    if bitstring == "01 11 11 01": return Card(3, 0)
    if bitstring == "01 01 01 11": return Card(4, 0)
    if bitstring == "11 11 01 01": return Card(5, 0)
    if bitstring == "11 01 11 01": return Card(6, 0)
    if bitstring == "11 01 01 11": return Card(7, 0)
    if bitstring == "01 01 11 01": return Card(8, 0)
    if bitstring == "01 11 01 11": return Card(9, 0)
    if bitstring == "01 01 11 11": return Card(10, 0)
    if bitstring == "01 11 11 11": return Card(11, 0)
    if bitstring == "11 01 11 11": return Card(12, 0)

    if bitstring == "10 11 11 11": return Card(0, 1)
    if bitstring == "11 10 11 11": return Card(1, 1)
    if bitstring == "11 11 10 11": return Card(2, 1)
    if bitstring == "11 11 11 10": return Card(3, 1)
    if bitstring == "11 11 11 11": return Card(4, 1)
    if bitstring == "10 01 01 01": return Card(5, 1)
    if bitstring == "01 10 01 01": return Card(6, 1)
    if bitstring == "01 01 10 01": return Card(7, 1)
    if bitstring == "01 01 01 10": return Card(8, 1)
    if bitstring == "10 10 01 01": return Card(9, 1)
    if bitstring == "10 01 10 01": return Card(10, 1)
    if bitstring == "10 01 01 10": return Card(11, 1)
    if bitstring == "01 10 10 01": return Card(12, 1)

    if bitstring == "01 10 11 11": return Card(0, 2)
    if bitstring == "01 01 10 10": return Card(1, 2)
    if bitstring == "01 10 10 10": return Card(2, 2)
    if bitstring == "10 01 10 10": return Card(3, 2)
    if bitstring == "10 10 01 10": return Card(4, 2)
    if bitstring == "10 10 10 01": return Card(5, 2)
    if bitstring == "10 11 01 01": return Card(6, 2)
    if bitstring == "10 01 11 01": return Card(7, 2)
    if bitstring == "10 01 01 11": return Card(8, 2)
    if bitstring == "11 10 01 01": return Card(9, 2)
    if bitstring == "01 10 11 01": return Card(10, 2)
    if bitstring == "01 10 01 11": return Card(11, 2)
    if bitstring == "11 01 10 01": return Card(12, 2)

    if bitstring == "11 11 01 11": return Card(0, 3)
    if bitstring == "11 11 11 01": return Card(1, 3)
    if bitstring == "10 10 10 10": return Card(2, 3)
    if bitstring == "11 10 10 10": return Card(3, 3)
    if bitstring == "10 11 10 10": return Card(4, 3)
    if bitstring == "10 10 11 10": return Card(5, 3)
    if bitstring == "10 10 10 11": return Card(6, 3)
    if bitstring == "11 11 10 10": return Card(7, 3)
    if bitstring == "11 10 11 10": return Card(8, 3)
    if bitstring == "11 10 10 11": return Card(9, 3)
    if bitstring == "10 11 11 10": return Card(10, 3)
    if bitstring == "10 11 10 11": return Card(11, 3)
    if bitstring == "10 10 11 11": return Card(12, 3)

    raise LookupError("Could not find card with code {}.".format(bitstring))
