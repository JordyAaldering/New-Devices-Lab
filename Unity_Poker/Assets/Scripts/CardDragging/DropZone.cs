using UnityEngine;
using UnityEngine.EventSystems;

public class DropZone : MonoBehaviour, IDropHandler, IPointerExitHandler
{
    [SerializeField] private Place place = Place.NULL;
    [SerializeField] private int maximumCards = 2;
    [SerializeField] private int currentCards = 0;
    
    /// <summary> Drops a card at the drop zone below the mouse. </summary>
    /// <param name="eventData"> The object that is being dragged. </param>
    public void OnDrop(PointerEventData eventData)
    {
        Draggable d = eventData.pointerDrag.GetComponent<Draggable>();

        if (currentCards < maximumCards)
        {
            if (transform.CompareTag("Burn"))
            {
                foreach (Transform child in transform.GetChild(0))
                {
                    child.gameObject.SetActive(false);
                }
            }
            
            d.parentToReturnTo = transform.GetChild(0);
            currentCards++;
            
            GameManager.instance.StartShowWarning(
                transform.CompareTag("Burn") ? "Card burned!" : $"Card {currentCards}/{maximumCards} added.");
            
            GameManager.instance.dealOrder.Enqueue(place);
        }
        else
        {
            GameManager.instance.StartShowWarning($"Maximum number of {maximumCards} cards reached.");
        }
    }

    /// <summary> Resets the drop location of the dragging card if the mouse exits a drop zone. </summary>
    /// <param name="eventData"> The object that is being dragged. </param>
    public void OnPointerExit(PointerEventData eventData)
    {
        if (eventData.pointerDrag != null)
        {
            Draggable d = eventData.pointerDrag.GetComponent<Draggable>();
            d.parentToReturnTo = null;
        }
    }
}
