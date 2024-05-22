def SetNeighboursDistances(MazeGrid, Rows, Cols, CurrentX, CurrentY):

    Neighbours = {}

    if CurrentY - 1 > 0 and not MazeGrid[CurrentX][CurrentY - 1]["Explored"] and MazeGrid[CurrentX][CurrentY]["Connections"]["Up"]: # Up
        Neighbours[len(Neighbours) + 1] = {"X" : CurrentX, "Y" : CurrentY - 1}
    if CurrentY + 1 <= Rows and not MazeGrid[CurrentX][CurrentY + 1]["Explored"] and MazeGrid[CurrentX][CurrentY]["Connections"]["Down"]: # Down
        Neighbours[len(Neighbours) + 1] = {"X" : CurrentX, "Y" : CurrentY + 1}
    if CurrentX - 1 > 0 and not MazeGrid[CurrentX - 1][CurrentY]["Explored"] and MazeGrid[CurrentX][CurrentY]["Connections"]["Left"]: # Left
        Neighbours[len(Neighbours) + 1] = {"X" : CurrentX - 1, "Y" : CurrentY}
    if CurrentX + 1 <= Cols and not MazeGrid[CurrentX + 1][CurrentY]["Explored"] and MazeGrid[CurrentX][CurrentY]["Connections"]["Right"]: # Right
        Neighbours[len(Neighbours) + 1] = {"X" : CurrentX + 1, "Y" : CurrentY}

    for Index in Neighbours:

        Position = Neighbours[Index]
        Distance = MazeGrid[Position["X"]][Position["Y"]]["Distance"]

        if MazeGrid[CurrentX][CurrentY]["Distance"] + 1 < Distance:

            MazeGrid[Position["X"]][Position["Y"]]["Distance"] = MazeGrid[CurrentX][CurrentY]["Distance"] + 1
            MazeGrid[Position["X"]][Position["Y"]]["Parent"] = {"X" : CurrentX, "Y" : CurrentY}

def GetLowestCell(MazeGrid, Rows, Cols):

    LowestX, LowestY = Cols, Rows

    for x in range(1, Cols + 1):
        for y in range(1, Rows + 1):
            if not MazeGrid[x][y]["Explored"] and MazeGrid[x][y]["Distance"] < MazeGrid[LowestX][LowestY]["Distance"]:
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

    MazeGrid[StartPos["X"]][StartPos["Y"]]["Distance"] = 0

    while not MazeGrid[EndPos["X"]][EndPos["Y"]]["Explored"]:
        
        CurrentX, CurrentY = GetLowestCell(MazeGrid, Rows, Cols)
        MazeGrid[CurrentX][CurrentY]["Explored"] = True
        
        SetNeighboursDistances(MazeGrid, Rows, Cols, CurrentX, CurrentY)

    return GetWaypoints(MazeGrid, StartPos, EndPos)