using UnityEngine;
using UnityEngine.EventSystems;

public class Draggable : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler
{
    public CanvasGroup canvasGroup;
    public Transform parentToReturnTo;

    /// <summary> Starts dragging a card. </summary>
    /// <param name="eventData"> The object that is being dragged. </param>
    public void OnBeginDrag(PointerEventData eventData)
    {
        parentToReturnTo = null;
        canvasGroup.blocksRaycasts = false;
    }

    /// <summary> Moves the dragging card to the mouse position. </summary>
    /// <param name="eventData"> The object that is being dragged. </param>
    public void OnDrag(PointerEventData eventData)
    {
        transform.position = eventData.position;
    }

    /// <summary> Places a card at the desired position or places it back at the deck. </summary>
    /// <param name="eventData"> The object that is being dragged. </param>
    public void OnEndDrag(PointerEventData eventData)
    {
        if (parentToReturnTo != null)
        {
            transform.SetParent(parentToReturnTo);
            canvasGroup.blocksRaycasts = true;
            Destroy(GetComponent<Draggable>());
        }
        else
        {
            Destroy(gameObject);
        }
    }
}
