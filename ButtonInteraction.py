using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;

public class Complete : MonoBehaviour
{
    ARRaycastManager arRaycastManager;
    bool planeIsDetected;
    Pose placementPose;
    public GameObject placementIndicator;
    GameObject objectToPlace;
    public GameObject blackChess;
    public GameObject whiteChess;
    public GameObject coffee;
    public GameObject instructions;
    public GameObject blackButton;
    public GameObject whiteButton;
    public GameObject coffeeButton;
    GameObject placedObject;
    bool isPlaced;

    void Start()
    {
        arRaycastManager = GetComponent<ARRaycastManager>();

        objectToPlace = blackChess;
        isPlaced = false;

        blackButton.GetComponent<Button>().onClick.AddListener(delegate { SwitchObjectToPlace(blackButton.name); });
        whiteButton.GetComponent<Button>().onClick.AddListener(delegate { SwitchObjectToPlace(whiteButton.name); });
        coffeeButton.GetComponent<Button>().onClick.AddListener(delegate { SwitchObjectToPlace(coffeeButton.name); });


    }


    void Update()
    {
        UpdatePlacementPose();
        UpdateUI();
        UpdatePlacementIndicator();

        // Input: https://docs.unity3d.com/ScriptReference/Input.html
        if (planeIsDetected && Input.touchCount == 1 && (Input.GetTouch(0).phase == TouchPhase.Began || Input.GetTouch(0).phase == TouchPhase.Moved))
        {
            if (!isPlaced)
            {
                PlaceObject(Input.GetTouch(0));
                isPlaced = true;
            }
            else
            {
                MoveObject(Input.GetTouch(0));
            }

        }
    }

    private void UpdatePlacementPose()
    {
        // ViewportToScreenPoint: https://docs.unity3d.com/ScriptReference/Camera.ViewportToScreenPoint.html 
        Vector3 screenCenter = Camera.main.ViewportToScreenPoint(new Vector2(0.5f, 0.5f));
        List<ARRaycastHit> hits = new List<ARRaycastHit>();
        // ARRaycastManager: https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@2.1/api/UnityEngine.XR.ARFoundation.ARRaycastManager.html
        arRaycastManager.Raycast(screenCenter, hits, TrackableType.PlaneWithinPolygon);

        planeIsDetected = hits.Count > 0;

        if (planeIsDetected)
        {
            // Pose: https://docs.unity3d.com/ScriptReference/Pose.html
            placementPose = hits[0].pose;
            // Transform.forward: https://docs.unity3d.com/ScriptReference/Transform-forward.html
            Vector3 cameraForward = Camera.main.transform.forward;
            // Vector3.normalized: https://docs.unity3d.com/ScriptReference/Vector3-normalized.html
            Vector3 cameraBearing = new Vector3(cameraForward.x, 0, cameraForward.z).normalized;
            // Quaternion.LookRotation: https://docs.unity3d.com/ScriptReference/Quaternion.LookRotation.html
            placementPose.rotation = Quaternion.LookRotation(cameraBearing);
        }
    }

    private void UpdatePlacementIndicator()
    {
        if (planeIsDetected && !isPlaced)
        {
            // GameObject.SetActive: https://docs.unity3d.com/ScriptReference/GameObject.SetActive.html
            placementIndicator.SetActive(true);
            placementIndicator.transform.SetPositionAndRotation(placementPose.position, placementPose.rotation);
        }
        else
        {
            placementIndicator.SetActive(false);
        }
    }


    private void PlaceObject(Touch touch)
    {
        if (!IsPointerOverUIObject(touch))
        {
            // Instantiate: https://docs.unity3d.com/ScriptReference/Object.Instantiate.html
            placedObject = Instantiate(objectToPlace, placementPose.position, placementPose.rotation);
        }

    }

    private void MoveObject(Touch touch)
    {
        if (!IsPointerOverUIObject(touch))
        {
            List<ARRaycastHit> hits = new List<ARRaycastHit>();
            arRaycastManager.Raycast(touch.position, hits, TrackableType.PlaneWithinPolygon);

            if (hits.Count > 0)
            {
                placedObject.transform.position = hits[0].pose.position;
                placedObject.transform.rotation = hits[0].pose.rotation;
            }
        }
    }

    private void SwitchObjectToPlace(string buttonName)
    {
        switch(buttonName)
        {
            case "blackButton":
                Destroy(placedObject);
                isPlaced = false;
                objectToPlace = blackChess;
                break;
            case "whiteButton":
                Destroy(placedObject);
                isPlaced = false;
                objectToPlace = whiteChess;
                break;
            case "coffeeButton":
                Destroy(placedObject);
                isPlaced = false;
                objectToPlace = coffee;
                break;
        }
    }

    // Helper function
    public static bool IsPointerOverUIObject(Touch touch)
    {
        PointerEventData eventDataCurrentPosition = new PointerEventData(EventSystem.current);
        eventDataCurrentPosition.position = new Vector2(touch.position.x, touch.position.y);
        List<RaycastResult> results = new List<RaycastResult>();
        EventSystem.current.RaycastAll(eventDataCurrentPosition, results);
        return results.Count > 0;
    }

    void UpdateUI()
    {
        if (planeIsDetected)
        {
            instructions.GetComponent<Text>().text = "Tap anywhere to place selected object\nUse one finger to drag and two fingers to rotate";
            blackButton.SetActive(true);
            whiteButton.SetActive(true);
            coffeeButton.SetActive(true);
        }
        else
        {
            instructions.GetComponent<Text>().text = "Move device around to find a plane";
            blackButton.SetActive(false);
            whiteButton.SetActive(false);
            coffeeButton.SetActive(false);
        }
    }

}
