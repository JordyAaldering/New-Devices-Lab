using System;

public class Card : IComparable<Card>
{
    public int suit { get; }
    public int rank { get; }

    private static readonly string[] suits = {"hearts", "spades", "diamonds", "clubs"};
    private static readonly string[] ranks = {"ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"};

    /// <summary> Initialises a new card. </summary>
    /// <param name="suit"> The suit as a number. </param>
    /// <param name="rank"> The rank as a number. </param>
    public Card(int suit, int rank)
    {
        this.suit = suit;
        this.rank = rank;
    }
    
    /// <summary> Gets the highest of two cards. </summary>
    /// <param name="a"> The first card. </param>
    /// <param name="b"> The second card. </param>
    /// <returns> The card with the highest card value. </returns>
    public static Card Max(Card a, Card b)
    {
        return a > b ? a : b;
    }

    /// <summary> Compares this card to another card. </summary>
    /// <param name="self"> This card. </param>
    /// <param name="other"> The card to compare to. </param>
    /// <returns> True if the card value of self is lower than the card value of other. </returns>
    public static bool operator <(Card self, Card other)
    {
        if (self.rank == 0)
        {
            return other.rank == 0 && self.suit < other.suit;
        }

        if (other.rank == 0)
        {
            return true;
        }

        return self.rank != other.rank ? self.rank < other.rank : self.suit < other.suit;
    }

    /// <summary> Compares this card to another card. </summary>
    /// <param name="self"> This card. </param>
    /// <param name="other"> The card to compare to. </param>
    /// <returns> True if the card value of self is higher than the card value of other. </returns>
    public static bool operator >(Card self, Card other)
    {
        if (self.rank == 0)
        {
            return other.rank != 0 || self.suit > other.suit;
        }

        if (other.rank == 0)
        {
            return false;
        }

        return self.rank != other.rank ? self.rank > other.rank : self.suit > other.suit;
    }
    
    /// <summary> Compares this card to another card. </summary>
    /// <param name="other"> The card to compare to. </param>
    /// <returns> -1 if the card value of this card is lower than other and 1 if it is higher. 0 otherwise. </returns>
    public int CompareTo(Card other)
    {
        if (this < other)
        {
            return -1;
        }

        if (this > other)
        {
            return 1;
        }

        return 0;
    }

    /// <summary> Turns this card into a string. </summary>
    /// <returns> This card as a string. </returns>
    public override string ToString()
    {
        return ranks[rank] + " of " + suits[suit];
    }
}
