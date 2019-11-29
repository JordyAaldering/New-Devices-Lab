using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;
using UnityEngine;

public class JsonManager : MonoBehaviour
{
    public static JsonManager instance { get; private set; }
    
    public string address = "";

    /// <summary> Creates a singleton JsonManager and makes sets it to not get destroyed on load. </summary>
    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(this);
        }
        else if (instance != this)
        {
            Destroy(gameObject);
        }
    }

    /// <summary> Checks if the Json page exists. </summary>
    /// <returns> True is the Json page exists, false otherwise. </returns>
    public bool JsonExists()
    {
        return Get(address) != null;
    }

    /// <summary> Reads a Json page and creates a deck if the page exists. </summary>
    public void ReadJson()
    {
        string data = Get(address);

        if (data != null)
        {
            int index = data.IndexOf("data", StringComparison.Ordinal);
            data = data.Substring(index);
            
            data = Regex.Replace(data, "[^.0-9]", "");
            Queue<Card> deck = string_to_deck(data);
            GameManager.instance.deck = deck;
        }
    }

    /// <summary> Gets data from a Json page. </summary>
    /// <param name="url"> The url of the Json page. </param>
    /// <returns> The data of the Json page if the page exists, null otherwise. </returns>
    private static string Get(string url) 
    {
        try
        {
            HttpWebRequest request = (HttpWebRequest) WebRequest.Create(url);
            WebResponse response = request.GetResponse();
            
            using (Stream responseStream = response.GetResponseStream())
            {
                if (responseStream != null)
                {
                    StreamReader reader = new StreamReader(responseStream, Encoding.UTF8);
                    return reader.ReadToEnd();
                }
            }
        }
        catch (WebException ex)
        {
            Debug.LogError(ex.ToString());
        }

        return null;
    }

    /// <summary> Turns a string into a deck. </summary>
    /// <param name="s"> The string. </param>
    /// <returns> A new deck. </returns>
    private static Queue<Card> string_to_deck(string s)
    {
        Queue<Card> deck = new Queue<Card>();
        
        for (int i = 0; i < s.Length; i += 2)
        {
            int num = (s[i] - '0') * 10 + (s[i + 1] - '0');
            Card card = new Card(Mathf.FloorToInt((float) (num - num % 13) / 13), num % 13);
            deck.Enqueue(card);
        }
        
        return deck;
    }
}
