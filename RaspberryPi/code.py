class Code:
    def __init__(self, bitstring):
        """
        Initialises this code.
        :param bitstring: The bitstring to turn into a code.
        """
        self.bits = [int(bit) for bit in bitstring.replace(" ", "")]

    @classmethod
    def from_card(cls, rank, suit):
        """
        Turns a card into a code.
        :param rank: The rank of the card.
        :param suit: The suit of the card.
        :return: A code corresponding to the card.
        """
        assert 0 <= rank < 13, "Rank index out of range."
        assert 0 <= suit < 4, "Suit index out of range."

        return cls(str(cls.from_rank(rank) + cls.from_suit(suit)))

    @classmethod
    def from_rank(cls, rank):
        """
        Turns a rank into a code.
        :param rank: The rank to get the code from.
        :return: A code corresponding to the rank.
        """
        assert 0 <= rank < 13, "Rank index out of range."
        return cls("".join(["01" if rank % 2 ** i < 2 ** i / 2 else "10" for i in range(4, 0, -1)]))

    @classmethod
    def from_suit(cls, suit):
        """
        Turns a suit into a code.
        :param suit: The suit to get the code from.
        :return: A code corresponding to the suit.
        """
        assert 0 <= suit < 4, "Suit index out of range."
        return cls("".join(["01" if suit >= i else "00" for i in range(3, -1, -1)]))

    def __add__(self, other):
        """
        Adds two codes.
        :param other: The other code.
        :return: The addition of this code and the other code.
        """
        bits = 8 * [int]

        for i in range(8):
            if i == 7:
                bits[7] = (self.bits[7] + other.bits[7]) % 2
            elif self.bits[i + 1] + other.bits[i + 1] == 2:
                bits[i] = (self.bits[i] + other.bits[i] + 1) % 2
            else:
                bits[i] = (self.bits[i] + other.bits[i]) % 2

        return Code("".join([str(b) for b in bits]))

    def __str__(self):
        """
        Turns this code into a string.
        :return: This code as a string.
        """
        return " ".join([str(self.bits[i]) + str(self.bits[i + 1]) for i in range(0, 8, 2)])


def main():
    """
    Prints all codes and checks if they are all unique.
    """
    codes = []

    for suit in range(4):
        for rank in range(13):
            code = str(Code.from_card(rank, suit))
            codes.append(code)
            print(code)

    print("All unique:", len(codes) != len(set(codes)))


if __name__ == "__main__":
    main()
