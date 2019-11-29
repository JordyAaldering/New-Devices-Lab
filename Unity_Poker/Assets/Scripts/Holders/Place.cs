using System.ComponentModel;

/// <summary> Describes the places a card can be dropped. </summary>
public enum Place
{
    [Description("Player 1")] PLAYER1,
    [Description("Player 2")] PLAYER2,
    [Description("Player 3")] PLAYER3,
    [Description("Player 4")] PLAYER4,
    [Description("Player 5")] PLAYER5,
    [Description("Player 6")] PLAYER6,
    [Description("Player 7")] PLAYER7,
    TABLE,
    BURN,
    NULL
}
