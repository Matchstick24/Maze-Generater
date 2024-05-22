import math

def GetDistance(p1, p2):

    Minus = {
        
        "X" : abs(p1["X"] - p2["X"]),
        "Y" : abs(p1["Y"] - p2["Y"]),

    }

    return math.sqrt(Minus["X"] ** 2 + Minus["Y"] ** 2)

def SetNeighboursDistances(MazeGrid, Rows, Cols, CurrentX, CurrentY):

    Neighbours = {}

    if CurrentY - 1 > 0 and not MazeGrid[CurrentX][CurrentY - 1]["Closed"] and MazeGrid[CurrentX][CurrentY]["Connections"]["Up"]: # Up
        Neighbours[len(Neighbours) + 1] = {"X" : CurrentX, "Y" : CurrentY - 1}
    if CurrentY + 1 <= Rows and not MazeGrid[CurrentX][CurrentY + 1]["Closed"] and MazeGrid[CurrentX][CurrentY]["Connections"]["Down"]: # Down
        Neighbours[len(Neighbours) + 1] = {"X" : CurrentX, "Y" : CurrentY + 1}
    if CurrentX - 1 > 0 and not MazeGrid[CurrentX - 1][CurrentY]["Closed"] and MazeGrid[CurrentX][CurrentY]["Connections"]["Left"]: # Left
        Neighbours[len(Neighbours) + 1] = {"X" : CurrentX - 1, "Y" : CurrentY}
    if CurrentX + 1 <= Cols and not MazeGrid[CurrentX + 1][CurrentY]["Closed"] and MazeGrid[CurrentX][CurrentY]["Connections"]["Right"]: # Right
        Neighbours[len(Neighbours) + 1] = {"X" : CurrentX + 1, "Y" : CurrentY}

    for Index in Neighbours:

        Position = Neighbours[Index]
        Cell = MazeGrid[Position["X"]][Position["Y"]]

        if MazeGrid[CurrentX][CurrentY]["Gcost"] + 1 < Cell["Gcost"] or not Cell["Open"]:

            Cell["Gcost"] = MazeGrid[CurrentX][CurrentY]["Gcost"] + 1
            Cell["Fcost"] = Cell["Gcost"] + Cell["Hcost"]
            Cell["Parent"] = {"X" : CurrentX, "Y" : CurrentY}
            Cell["Open"] = True
 
def GetLowestCell(MazeGrid, Rows, Cols):

    LowestX, LowestY = 1, 1

    for x in range(1, Cols + 1):
        for y in range(1, Rows + 1):

            Cell = MazeGrid[x][y]

            if Cell["Open"]:
                if Cell["Fcost"] < MazeGrid[LowestX][LowestY]["Fcost"] or Cell["Hcost"] < MazeGrid[LowestX][LowestY]["Hcost"]:
 
                    LowestX, LowestY = x, y

    return LowestX, LowestY

def GetWaypoints(MazeGrid, StartPos, EndPos):

    Waypoints = {}
    CurrentPos = {"X" : EndPos["X"], "Y" : EndPos["Y"]}
    Waypoints[len(Waypoints) + 1] = {"X" : EndPos["X"] * 2, "Y" : EndPos["Y"] * 2}

    while CurrentPos != StartPos:

        Waypoints[len(Waypoints) + 1] = {"X" : CurrentPos["X"] * 2, "Y" : CurrentPos["Y"] * 2}
        CurrentPos = MazeGrid[CurrentPos["X"]][CurrentPos["Y"]]["Parent"]

    Waypoints[len(Waypoints) + 1] = {"X" : 2, "Y" : 2}
    FixedWaypoints = {}

    for Waypoint in range(len(Waypoints), 1, -1): 

        FixedWaypoints[len(FixedWaypoints) + 1] = Waypoints[Waypoint]

    return FixedWaypoints

def FindPath(MazeGrid, Rows, Cols, StartPos, EndPos):

    for x in range(1, Cols + 1):
        for y in range(1, Rows + 1):

            MazeGrid[x][y]["Gcost"] = GetDistance(MazeGrid[x][y], MazeGrid[StartPos["X"]][StartPos["Y"]])
            MazeGrid[x][y]["Hcost"] = GetDistance(MazeGrid[x][y], MazeGrid[EndPos["X"]][EndPos["Y"]])
            MazeGrid[x][y]["Fcost"] = MazeGrid[x][y]["Gcost"] + MazeGrid[x][y]["Hcost"]

    MazeGrid[StartPos["X"]][StartPos["Y"]]["Open"] = True

    while True:
        
        CurrentX, CurrentY = GetLowestCell(MazeGrid, Rows, Cols)
        MazeGrid[CurrentX][CurrentY]["Open"] = False
        MazeGrid[CurrentX][CurrentY]["Closed"] = True

        if CurrentX == EndPos["X"] and CurrentY == EndPos["Y"]:
            break
        
        SetNeighboursDistances(MazeGrid, Rows, Cols, CurrentX, CurrentY)

    return GetWaypoints(MazeGrid, StartPos, EndPos)