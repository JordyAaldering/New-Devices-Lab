using System.Collections.Generic;
using UnityEngine;

public class Evaluator
{
    private readonly Dictionary<Place, Hand> players;
    private readonly Dictionary<Place, BestHand> bestHands;
    private readonly Dictionary<Place, Card> bestPairCards;
    
    /// <summary> Initialises a new evaluator. </summary>
    /// <param name="players"> A dictionary of players and the corresponding hands. </param>
    public Evaluator(Dictionary<Place, Hand> players)
    {
        this.players = players;
        bestHands = new Dictionary<Place, BestHand>();
        bestPairCards = new Dictionary<Place, Card>();
        
        foreach (KeyValuePair<Place, Hand> pair in players)
        {
            pair.Value.Sort();
        }
    }

    /// <summary> Evaluates the player hands. </summary>
    public void Evaluate()
    {
        foreach (KeyValuePair<Place, Hand> pair in players)
        {
            BestHand bestHand = EvaluateHand(pair.Value, out Card bestPairCard);
            
            bestHands.Add(pair.Key, bestHand);
            bestPairCards.Add(pair.Key, bestPairCard);
        }
    }

    /// <summary> Gets the best hand out of all hands. </summary>
    /// <returns> The player with the best hand and the corresponding deck. </returns>
    public KeyValuePair<Place, BestHand> GetBestHand()
    {
        Place bestPlace = Place.NULL;
        BestHand bestHand = BestHand.NULL;

        foreach (KeyValuePair<Place, BestHand> pair in bestHands)
        {
            if (bestPlace == Place.NULL)
            {
                bestPlace = pair.Key;
                bestHand = pair.Value;
            }
            else if ((int) pair.Value > (int) bestHand)
            {
                // This hand is better than the current best hand.
                bestPlace = pair.Key;
                bestHand = pair.Value;
            }
            else if ((int) pair.Value == (int) bestHand)
            {
                // This hand is just as good as the current best hand.
                if (Max(pair.Key, bestPlace) == pair.Key)
                {
                    // The hand with the best high card wins.
                    bestPlace = pair.Key;
                    bestHand = pair.Value;
                }
            }
        }

        return new KeyValuePair<Place, BestHand>(bestPlace, bestHand);
    }

    /// <summary> Removes the hand of a player. </summary>
    /// <param name="place"> The player whose deck to remove. </param>
    public void Remove(Place place)
    {
        bestHands.Remove(place);
    }

    /// <summary> Gets the number of players. </summary>
    /// <returns> The number of players. </returns>
    public int Length()
    {
        return players.Count;
    }

    /// <summary> Gets the best hand of the player and the corresponding highest card of that hand. </summary>
    /// <param name="hand"> The hand to evaluate. </param>
    /// <param name="bestPairCard"> The highest card of a hand. </param>
    /// <returns> The best possible hand. </returns>
    private static BestHand EvaluateHand(Hand hand, out Card bestPairCard)
    {
        if (RoyalFlush(hand, out bestPairCard))
        {
            return BestHand.ROYAL_FLUSH;
        }
        else if (StraightFlush(hand, out bestPairCard))
        {
            return BestHand.STRAIGHT_FLUSH;
        }
        else if (FourOfAKind(hand, out bestPairCard))
        {
            return BestHand.FOUR_OF_A_KIND;
        }
        else if (FullHouse(hand, out bestPairCard))
        {
            return BestHand.FULL_HOUSE;
        }
        else if (Flush(hand, out bestPairCard))
        {
            return BestHand.FLUSH;
        }
        else if (Straight(hand, out bestPairCard))
        {
            return BestHand.STRAIGHT;
        }
        else if (ThreeOfAKind(hand, out bestPairCard))
        {
            return BestHand.THREE_OF_A_KIND;
        }
        else if (TwoPair(hand, out bestPairCard))
        {
            return BestHand.TWO_PAIR;
        }
        else if (OnePair(hand, out bestPairCard))
        {
            return BestHand.ONE_PAIR;
        }

        bestPairCard = hand.Max();
        return BestHand.HIGH_CARD;
    }

    /// <summary> Checks if this hand has a Royal Flush. </summary>
    /// <param name="hand"> The hand to evaluate. </param>
    /// <param name="bestPairCard"> The highest card of a hand. </param>
    /// <returns> True if this hand has a Royal Flush, false otherwise. </returns>
    private static bool RoyalFlush(Hand hand, out Card bestPairCard)
    {
        bestPairCard = new Card(0, 1);
        int length = 0;
        
        for (int i = 0; i < hand.length() - 1; i++)
        for (int j = i + 1; j < hand.length(); j++)
        {
            if (length == 0 && hand.Get(i).rank != 9)
            {
                break;
            }
            
            // The current card is one lower than the next card.
            // Or the current card is a king and the next card is an ace.
            if (hand.Get(i).rank + 1 == hand.Get(j).rank || hand.Get(i).rank == 12 && hand.Get(j).rank == 0)
            {
                if (hand.Get(i).rank + 1 == hand.Get(j).rank || hand.Get(i).rank == 12 && hand.Get(j).rank == 0)
                {
                    bestPairCard = hand.Get(j);
                    length++;
                }
                else if (length >= 5)
                {
                    bestPairCard = hand.Get(j);
                    return true;
                }
                else
                {
                    i = j;
                    break;
                }
            }
        }

        return length >= 5 && Straight(hand, out bestPairCard);
    }
    
    /// <summary> Checks if this hand has a Straight Flush. </summary>
    /// <param name="hand"> The hand to evaluate. </param>
    /// <param name="bestPairCard"> The highest card of a hand. </param>
    /// <returns> True if this hand has a Straight Flush, false otherwise. </returns>
    private static bool StraightFlush(Hand hand, out Card bestPairCard)
    {
        bool straight = Straight(hand, out Card bestPairCard1);
        straight = Flush(hand, out Card bestPairCard2) && straight;
        if (straight)
        {
            bestPairCard = Card.Max(bestPairCard1, bestPairCard2);
            return true;
        }

        bestPairCard = new Card(0, 1);
        return false;
    }

    /// <summary> Checks if this hand has a Four of a Kind. </summary>
    /// <param name="hand"> The hand to evaluate. </param>
    /// <param name="bestPairCard"> The highest card of a hand. </param>
    /// <returns> True if this hand has a Four of a Kind, false otherwise. </returns>
    private static bool FourOfAKind(Hand hand, out Card bestPairCard)
    {
        for (int i = 3; i < hand.length(); i++)
        {
            if (hand.Get(i - 3).rank == hand.Get(i - 2).rank && hand.Get(i - 2).rank == hand.Get(i - 1).rank &&
                hand.Get(i - 1).rank == hand.Get(i).rank)
            {
                bestPairCard = hand.Get(i);
                return true;
            }
        }

        bestPairCard = new Card(0, 1);
        return false;
    }

    /// <summary> Checks if this hand has a Full House. </summary>
    /// <param name="hand"> The hand to evaluate. </param>
    /// <param name="bestPairCard"> The highest card of a hand. </param>
    /// <returns> True if this hand has a Full House, false otherwise. </returns>
    private static bool FullHouse(Hand hand, out Card bestPairCard)
    {
        bestPairCard = new Card(0, 1);
        bool twoOfAKind = false;
        bool threeOfAKind = false;
        
        for (int i = 0; i < hand.length() - 2; i++)
        {
            if (threeOfAKind == false && hand.Get(i).rank == hand.Get(i + 1).rank &&
                hand.Get(i + 1).rank == hand.Get(i + 2).rank)
            {
                bestPairCard = hand.Get(i + 2);
                threeOfAKind = true;
                i += 2;
            }
            else if (twoOfAKind == false && hand.Get(i).rank == hand.Get(i + 1).rank)
            {
                bestPairCard = hand.Get(i + 1);
                twoOfAKind = true;
                i++;
            }
        }

        return twoOfAKind && threeOfAKind;
    }

    /// <summary> Checks if this hand has a Flush. </summary>
    /// <param name="hand"> The hand to evaluate. </param>
    /// <param name="bestPairCard"> The highest card of a hand. </param>
    /// <returns> True if this hand has a Flush, false otherwise. </returns>
    private static bool Flush(Hand hand, out Card bestPairCard)
    {
        int hearts = 0, spades = 0, diamonds = 0, clubs = 0;
        
        for (int i = 0; i < hand.length(); i++)
        {
            switch (hand.Get(i).suit)
            {
                case 0:
                    hearts++;
                    break;
                case 1:
                    spades++;
                    break;
                case 2:
                    diamonds++;
                    break;
                case 3:
                    clubs++;
                    break;
                default:
                    Debug.LogError("Unknown suit.");
                    break;
            }
        }

        bestPairCard = new Card(0, 1);
        return hearts >= 5 || spades >= 5 || diamonds >= 5 || clubs >= 5;
    }

    /// <summary> Checks if this hand has a Straight. </summary>
    /// <param name="hand"> The hand to evaluate. </param>
    /// <param name="bestPairCard"> The highest card of a hand. </param>
    /// <returns> True if this hand has a Straight, false otherwise. </returns>
    private static bool Straight(Hand hand, out Card bestPairCard)
    {
        bestPairCard = new Card(0, 1);
        int length = 0;
        
        for (int i = 0; i < hand.length() - 1; i++)
        for (int j = i + 1; j < hand.length(); j++)
        {
            // The current card is one lower than the next card.
            // Or the current card is a king and the next card is an ace.
            if (hand.Get(i).rank + 1 == hand.Get(j).rank || hand.Get(i).rank == 12 && hand.Get(j).rank == 0)
            {
                bestPairCard = hand.Get(j);
                length++;
            }
            else if (length >= 5)
            {
                bestPairCard = hand.Get(j);
                return true;
            }
            else
            {
                bestPairCard = new Card(0, 1);
                i = j;
                break;
            }
        }

        if (length >= 5)
        {
            return true;
        }
        else
        {
            bestPairCard = new Card(0, 1);
            return false;
        }
    }

    /// <summary> Checks if this hand has a Three of a Kind. </summary>
    /// <param name="hand"> The hand to evaluate. </param>
    /// <param name="bestPairCard"> The highest card of a hand. </param>
    /// <returns> True if this hand has a Three of a Kind, false otherwise. </returns>
    private static bool ThreeOfAKind(Hand hand, out Card bestPairCard)
    {
        for (int i = 2; i < hand.length(); i++)
        {
            if (hand.Get(i - 2).rank == hand.Get(i - 1).rank && hand.Get(i - 1).rank == hand.Get(i).rank)
            {
                bestPairCard = hand.Get(i);
                return true;
            }
        }

        bestPairCard = new Card(0, 1);
        return false;
    }

    /// <summary> Checks if this hand has a Two Pair. </summary>
    /// <param name="hand"> The hand to evaluate. </param>
    /// <param name="bestPairCard"> The highest card of a hand. </param>
    /// <returns> True if this hand has a Two Pair, false otherwise. </returns>
    private static bool TwoPair(Hand hand, out Card bestPairCard)
    {
        bestPairCard = new Card(0, 1);
        bool onePair = false;
        bool twoPair = false;
        
        for (int i = 1; i < hand.length(); i++)
        {
            if (hand.Get(i - 1).rank == hand.Get(i).rank)
            {
                bestPairCard = hand.Get(i);
                twoPair = onePair;
                onePair = true;
                i++;
            }
        }

        return twoPair;
    }

    /// <summary> Checks if this hand has a One Pair. </summary>
    /// <param name="hand"> The hand to evaluate. </param>
    /// <param name="bestPairCard"> The highest card of a hand. </param>
    /// <returns> True if this hand has a One Pair, false otherwise. </returns>
    private static bool OnePair(Hand hand, out Card bestPairCard)
    {
        for (int i = 1; i < hand.length(); i++)
        {
            if (hand.Get(i - 1).rank == hand.Get(i).rank)
            {
                bestPairCard = hand.Get(i);
                return true;
            }
        }

        bestPairCard = new Card(0, 1);
        return false;
    }

    /// <summary> Gets the highest of two places. </summary>
    /// <param name="a"> The first place. </param>
    /// <param name="b"> The second place. </param>
    /// <returns> The place with the best hand. </returns>
    private Place Max(Place a, Place b)
    {
        if (bestPairCards[a] > bestPairCards[b])
        {
            return a;
        }
        
        return players[a].Max() > players[b].Max() ? a : b;
    }
}
