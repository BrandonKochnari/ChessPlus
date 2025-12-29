using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using static UnityEngine.Tilemaps.Tilemap;

public class PlayerBehaviour : MonoBehaviour
{
    [Header("Controllers")]
    private Keyboard keyboard;
    private Mouse mouse;

    [Header("Components")]
    private bool initClick;
    private bool dragged;
    public int row;
    public int col;
    private bool firstMove;
    public bool whitePiece;
    public Rigidbody2D rb;
    private GameObject lastValidTile;

    void Start()
    {
        mouse = Mouse.current;
        keyboard = Keyboard.current;
        initClick = false;
        dragged = false;
        firstMove = true;

        GameObject[] tiles = GameObject.FindGameObjectsWithTag("Tile");
        foreach (GameObject tile in tiles)
        {
            if (tile.GetComponent<Collider2D>().OverlapPoint(this.transform.position))
            {
                lastValidTile = tile;
        }
    }
}

    void FixedUpdate()
    {
        Vector2 mousePosition = Camera.main.ScreenToWorldPoint(mouse.position.value);

        if (dragged)
        {
            this.transform.position = mousePosition;
        }

        if (mouse.leftButton.isPressed == true && !initClick)
        {
            initClick = true;
            if (GetComponent<Collider2D>().OverlapPoint(mousePosition))
            {
                Debug.Log("clicked on box");
                dragged = true;
            }
        }

        else if (mouse.leftButton.isPressed == false)
        {
            initClick = false;
            if (dragged)
            {
                dragged = false;
                SnapToGrid(mousePosition);
            }

        }
    }

    private Vector3 MoveCorrection(GameObject srcTile, GameObject trgtTile)
    {
        int rowDiff = srcTile.GetComponent<TileInfo>().row - trgtTile.GetComponent<TileInfo>().row;
        int colDiff = srcTile.GetComponent<TileInfo>().col - trgtTile.GetComponent<TileInfo>().col;

        if (colDiff != 0)
            return srcTile.transform.position;

        if (whitePiece)
        {
            if (firstMove)
            {
                if (rowDiff >= -2 && rowDiff < 0)
                    return trgtTile.transform.position;
            }
            else
            {
                if (rowDiff == -1)
                    return trgtTile.transform.position;
            }
        }
        else
        {
            if (firstMove)
            {
                if (rowDiff <= 2 && rowDiff > 0)
                    return trgtTile.transform.position;
            }
            else
            {
                if (rowDiff == 1)
                    return trgtTile.transform.position;
            }
        }

        return srcTile.transform.position;
    }

    private void SnapToGrid(Vector2 mouse)
    {
        GameObject[] tiles = GameObject.FindGameObjectsWithTag("Tile");

        foreach(GameObject tile in tiles)
        {
            if (tile.GetComponent<Collider2D>().OverlapPoint(mouse))
            {
                int targetRow = tile.GetComponent<TileInfo>().row;
                int targetCol = tile.GetComponent<TileInfo>().col;
                this.transform.position = MoveCorrection(lastValidTile, tile);
            }
        }
    }
}
