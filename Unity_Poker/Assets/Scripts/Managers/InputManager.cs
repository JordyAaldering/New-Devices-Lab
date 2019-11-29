using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class InputManager : MonoBehaviour
{
    private Text warningText;

    private void Start()
    {
        warningText = GameObject.FindGameObjectWithTag("WarningText").GetComponent<Text>();
    }

    /// <summary> Updates the address of the Json page. </summary>
    /// <param name="s"> The new IP address. </param>
    public void UpdateText(string s)
    {
        JsonManager.instance.address = "http://" + s + ":8080/";
    }

    /// <summary> Loads the next scene if the Json exists, shows a warning otherwise. </summary>
    public void LoadScene()
    {
        if (JsonManager.instance.JsonExists())
        {
            SceneManager.LoadScene(1);
        }
        else
        {
            warningText.enabled = true;
            StartCoroutine(DisableText());
        }
    }

    /// <summary> Disables the warning text after two seconds. </summary>
    private IEnumerator DisableText()
    {
        yield return new WaitForSeconds(2f);
        warningText.enabled = false;
    }

    /// <summary> Quits the application. </summary>
    public void Quit()
    {
        Application.Quit();
    }
}
