using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public GameObject brownTilePrefab;
    public GameObject tanTilePrefab;
    public GameObject[] whitePiecePrefabs;
    public GameObject[] blackPiecePrefabs;

    // Start is called before the first frame update
    void Start()
    {
        // Setup tiles
        for (int row = 0; row < 8; row++)
        {
            for (int col = 0; col < 8; col++)
            {
                GameObject tileInstance;
                int index = row * 7 + col;
                if (index % 2 == 0)
                {
                    tileInstance = Instantiate(brownTilePrefab);
                }
                else
                {
                    tileInstance = Instantiate(tanTilePrefab);
                }
                tileInstance.transform.position = new Vector3(-4 + col + 0.5F, 4 - row - 0.5F, 0);
                tileInstance.GetComponent<TileInfo>().row = row;
                tileInstance.GetComponent<TileInfo>().col = col;
                tileInstance.GetComponent<SpriteRenderer>().sortingOrder = 1;
                tileInstance.transform.parent = GameObject.Find("AllTiles").transform;
            }
        }

        // Setup pieces
        int[] rows = new int[] { 0, 1, 6, 7 };
        foreach (int row in rows)
        {
            for (int col = 0; col < 8; col++)
            {
                GameObject[] allegiance = row < 4 ? whitePiecePrefabs : blackPiecePrefabs;
                GameObject newPiece = null;
                switch (row)
                {
                    case 0:
                        newPiece = Instantiate(allegiance[col < 5 ? col + 1 : 4 - (col - 4)]);
                        break;
                    case 1:
                        newPiece = Instantiate(allegiance[0]);
                        break;
                    case 6:
                        newPiece = Instantiate(allegiance[0]);
                        break;
                    case 7:
                        newPiece = Instantiate(allegiance[col < 5 ? col + 1 : 4 - (col - 4)]);
                        break;
                }
                if (newPiece == null)
                {
                    return;
                }
                newPiece.transform.position = new Vector3(-4 + col + 0.5F, 4 - row - 0.5F, 0);
                PlayerBehaviour pb = newPiece.GetComponent<PlayerBehaviour>();
                pb.row = row;
                pb.col = col;
                pb.whitePiece = row < 4 ? true : false;
                newPiece.GetComponent<SpriteRenderer>().sortingOrder = 2;
                newPiece.transform.parent = GameObject.Find("AllPieces").transform;
            }
        }
    }

    // Update is called once per frame
    void Update()
    {

    }
}