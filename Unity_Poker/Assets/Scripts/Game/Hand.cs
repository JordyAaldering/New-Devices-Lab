using System;
using System.Linq;

public class Hand
{
    private int index;
    private readonly Card[] hand;

    /// <summary> Initialises a new hand. </summary>
    /// <param name="size"> The size of the new hand. </param>
    public Hand(int size)
    {
        hand = new Card[size];
    }

    /// <summary> Adds a card to this hand. </summary>
    /// <param name="card"> The card to add. </param>
    public void Add(Card card)
    {
        hand[index++] = card;
    }

    /// <summary> Adds a card to this hand. </summary>
    /// <param name="i"> The card index to get. </param>
    /// <returns> The card at index i. </returns>
    public Card Get(int i)
    {
        return hand[i];
    }

    /// <summary> Gets the length of this hand. </summary>
    /// <returns> The amount of cards in this hand. </returns>
    public int length()
    {
        return index;
    }

    /// <summary> Gets the card with the highest value. </summary>
    /// <returns> The card with the highest value. </returns>
    public Card Max()
    {
        return hand.Min().rank == 0 ? hand.Min() : hand.Max();
    }

    /// <summary> Sorts the hand. </summary>
    public void Sort()
    {
        Array.Sort(hand);
    }

    /// <summary> Adds two hands. </summary>
    /// <param name="a"> This first hand. </param>
    /// <param name="b"> The second hand. </param>
    /// <returns> A new hand containing the cards of both hands. </returns>
    public static Hand operator +(Hand a, Hand b)
    {
        Hand h = new Hand(a.length() + b.length());
        
        for (int i = 0; i < a.length(); i++)
        {
            h.Add(a.Get(i));
        }
        
        for (int i = 0; i < b.length(); i++)
        {
            h.Add(b.Get(i));
        }
        
        return h;
    }

    /// <summary> Turns this hand into a string. </summary>
    /// <returns> This hand as a string. </returns>
    public override string ToString()
    {
        return hand.Aggregate("", (current, card) => current + (card + ", "));
    }
}
