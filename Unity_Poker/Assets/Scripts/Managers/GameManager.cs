using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class GameManager : MonoBehaviour
{
    public static GameManager instance { get; private set; }

    private Text warningText;
    private IEnumerator coroutine;
    
    public Queue<Card> deck = new Queue<Card>();
    public Queue<Place> dealOrder = new Queue<Place>();
    private readonly Dictionary<Place, Hand> hands = new Dictionary<Place, Hand>(9);
    
    private static CardDropZones cardDropZones;
    private static CardGraphics cardGraphics;

    /// <summary> Creates a singleton of this GameManager. </summary>
    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
        else if (instance != this)
        {
            Destroy(gameObject);
        }
    }

    /// <summary> Gets the components at the start of the scene. </summary>
    private void Start()
    {
        cardDropZones = GetComponent<CardDropZones>();
        cardGraphics = GetComponent<CardGraphics>();

        warningText = GameObject.Find("Warning Text").GetComponent<Text>();
    }

    /// <summary> Loads a scene. </summary>
    /// <param name="sceneIndex"> The index of the scene to load. </param>
    public void LoadScene(int sceneIndex)
    {
        SceneManager.LoadScene(sceneIndex);
    }

    /// <summary> Checks if the input is valid and evaluates the hands if it is. </summary>
    /// <param name="button"> The button that called this function. </param>
    public void DoneDealing(GameObject button)
    {
        if (CheckInput() == false) return;
        
        GameObject.FindGameObjectWithTag("TableText").SetActive(false);
        GameObject.FindWithTag("PullDeck").SetActive(false);
        GameObject.FindWithTag("Burn").SetActive(false);
        button.SetActive(false);

        JsonManager.instance.ReadJson();
        DealCards();
        SetSprites();
        Evaluate();
    }

    /// <summary> Checks if the user's input is valid. </summary>
    /// <returns> True if the input is valid, false otherwise. </returns>
    private bool CheckInput()
    {
        int[] cardCounts = {0, 0, 0, 0, 0, 0, 0, 0};
        foreach (Place place in dealOrder)
        {
            if (place != Place.BURN)
            {
                cardCounts[(int) place]++;
            }
        }
        
        bool playerFound = false;
        for (int i = 0; i < 8; i++)
        {
            if (cardCounts[i] == 1)
            {
                StartShowWarning("Players must have 2 cards.");
                return false;
            }
            
            if (cardCounts[i] == 2)
            {
                playerFound = true;
            }
        }

        if (cardCounts[(int) Place.TABLE] < 3)
        {
            StartShowWarning("The table must have at least 3 cards.");
            return false;
        }

        if (playerFound == false)
        {
            StartShowWarning("At least one player is required.");
            return false;
        }

        return true;
    }

    /// <summary> Starts a warning coroutine. </summary>
    /// <param name="warning"> The warning text. </param>
    public void StartShowWarning(string warning)
    {
        if (coroutine != null)
        {
            StopCoroutine(coroutine);
        }
            
        coroutine = ShowWarning(warning);
        StartCoroutine(coroutine);
    }

    /// <summary> Shows a warning text. </summary>
    /// <param name="warning"> The warning text. </param>
    private IEnumerator ShowWarning(string warning)
    {
        warningText.text = warning;
        warningText.enabled = true;
        
        yield return new WaitForSeconds(1f);

        warningText.enabled = false;
    }
    
    private void DealCards()
    {
        while (dealOrder.Count > 0)
        {
            Place key = dealOrder.Dequeue();
            
            if (hands.ContainsKey(key) == false)
            {
                switch (key)
                {
                    case Place.BURN:
                        hands.Add(key, new Hand(52));
                        break;
                    case Place.TABLE:
                        hands.Add(key, new Hand(5));
                        break;
                    default:
                        hands.Add(key, new Hand(2));
                        break;
                }
            }

            hands[key].Add(deck.Dequeue());
        }

        hands.Remove(Place.BURN);
    }

    /// <summary> Sets the sprites of the table players' hands. </summary>
    private void SetSprites()
    {
        foreach (KeyValuePair<Place, Hand> pair in hands)
        {
            SetHandSprites(
                (int) pair.Key <= (int) Place.PLAYER7 ? cardDropZones.players[(int) pair.Key] : cardDropZones.table,
                pair.Value);
        }
    }

    /// <summary> Sets the sprites of a players' hand. </summary>
    private static void SetHandSprites(GameObject place, Hand hand)
    {
        for (int i = 0; i < hand.length(); i++)
        {
            place.transform.GetChild(i).GetComponent<Image>().sprite = CardToSprite(hand.Get(i));
        }
    }

    /// <summary> Gets a card from a sprite. </summary>
    /// <param name="card"> The card to get the sprite of. </param>
    /// <returns> A sprite corresponding to the card. </returns>
    private static Sprite CardToSprite(Card card)
    {
        switch (card.suit)
        {
            case 0:
                return cardGraphics.hearts[card.rank];
            case 1:
                return cardGraphics.spades[card.rank];
            case 2:
                return cardGraphics.diamonds[card.rank];
            case 3:
                return cardGraphics.clubs[card.rank];
            default:
                Debug.LogError("Unknown card type!");
                return null;
        }
    }
    
    /// <summary> Evaluates the hands and finds the winners. </summary>
    private void Evaluate()
    {
        Dictionary<Place, Hand> players = new Dictionary<Place, Hand>();
        foreach (KeyValuePair<Place, Hand> pair in hands)
        {
            if ((int) pair.Key <= (int) Place.PLAYER7)
            {
                players.Add(pair.Key, pair.Value + hands[Place.TABLE]);
            }
        }
        
        Evaluator eval = new Evaluator(players);
        eval.Evaluate();
        SetWinnerSprites(eval);
    }

    /// <summary> Gets the winners from the evaluated hands and sets the corresponding sprites. </summary>
    /// <param name="eval"> The evaluated hands. </param>
    private void SetWinnerSprites(Evaluator eval)
    {
        KeyValuePair<Place, BestHand> firstPlace = eval.GetBestHand();
        Debug.Log(firstPlace.Key.GetDescription() + " comes second with a " + firstPlace.Value.GetDescription());
        
        StopCoroutine(coroutine);
        warningText.text = firstPlace.Key.GetDescription() + " wins with a " + firstPlace.Value.GetDescription();
        warningText.enabled = true;
        
        cardGraphics.crownLocations[(int) firstPlace.Key].GetComponent<Image>().enabled = true;
        cardGraphics.crownLocations[(int) firstPlace.Key].GetComponent<Image>().sprite = cardGraphics.crownGold;
        eval.Remove(firstPlace.Key);
        
        if (eval.Length() >= 2)
        {
            KeyValuePair<Place, BestHand> secondPlace = eval.GetBestHand();
            Debug.Log(secondPlace.Key.GetDescription() + " comes second with a " + secondPlace.Value.GetDescription());
            
            cardGraphics.crownLocations[(int) secondPlace.Key].GetComponent<Image>().enabled = true;
            cardGraphics.crownLocations[(int) secondPlace.Key].GetComponent<Image>().sprite = cardGraphics.crownSilver;
            eval.Remove(secondPlace.Key);
        }
        
        if (eval.Length() >= 3)
        {
            KeyValuePair<Place, BestHand> thirdPlace = eval.GetBestHand();
            Debug.Log(thirdPlace.Key.GetDescription() + " comes third with a " + thirdPlace.Value.GetDescription());
            
            cardGraphics.crownLocations[(int) thirdPlace.Key].GetComponent<Image>().enabled = true;
            cardGraphics.crownLocations[(int) thirdPlace.Key].GetComponent<Image>().sprite = cardGraphics.crownBronze;
        }
    }

    /// <summary> Turns this game manager into a string. </summary>
    /// <returns> This game manager as a string. </returns>
    public override string ToString()
    {
        string s = "";
        foreach (KeyValuePair<Place, Hand> pair in hands)
        {
            s += pair.Key + " " + pair.Value;
        }
        return s;
    }
}
