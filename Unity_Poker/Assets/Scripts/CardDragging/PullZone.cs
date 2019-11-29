using UnityEngine;
using UnityEngine.EventSystems;

public class PullZone : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler, IDropHandler
{
    public GameObject draggableCard;
    private GameObject currentlyDragging;
    
    /// <summary> Spawns a draggable card when a mouse enters the pull zone. </summary>
    /// <param name="eventData"> The object that is being dragged. </param>
    public void OnPointerEnter(PointerEventData eventData)
    {
        currentlyDragging = Instantiate(draggableCard, transform);
    }

    /// <summary> Removes the spawned card if the mouse exits without dragging. </summary>
    /// <param name="eventData"> The object that is being dragged. </param>
    public void OnPointerExit(PointerEventData eventData)
    {
        if (Input.GetMouseButton(0) == false)
        {
            Destroy(currentlyDragging);
        }
    }

    /// <summary> Removes the spawned card if the mouse drops a card back in the pull zone. </summary>
    /// <param name="eventData"> The object that is being dragged. </param>
    public void OnDrop(PointerEventData eventData)
    {
        if (currentlyDragging != null)
        {
            Destroy(currentlyDragging);
        }
    }
}
