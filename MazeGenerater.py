from random import randint
import math

Stack = {}

def CheckNeighbours(MazeGrid, CellGrid, x, y, Rows, Cols):

    Rows = math.floor(Rows / 2) + 1
    Cols = math.floor(Cols / 2) + 1

    Neighbours = {}

    if y - 1 != 0 and not MazeGrid[x][y - 1]["Visited"]: # Up

        Neighbours[len(Neighbours) + 1] = MazeGrid[x][y - 1]

    if y + 1 < Rows and not MazeGrid[x][y + 1]["Visited"]: # Down

        Neighbours[len(Neighbours) + 1] = MazeGrid[x][y + 1]

    if x + 1 < Cols and not MazeGrid[x + 1][y]["Visited"]: # Right

        Neighbours[len(Neighbours) + 1] = MazeGrid[x + 1][y]
    
    if x - 1 != 0 and not MazeGrid[x - 1][y]["Visited"]: # Left

        Neighbours[len(Neighbours) + 1] = MazeGrid[x - 1][y]

    if len(Neighbours) > 0:

        RandomNumber = randint(1, len(Neighbours))
        NextCell = Neighbours[RandomNumber]
        Stack[len(Stack) + 1] = NextCell

        if y - 1 != 0 and not MazeGrid[x][y - 1]["Visited"] and MazeGrid[x][y - 1] == NextCell: # Up

            CellGrid[x * 2][y * 2 - 1]["IsWall"] = False    
            MazeGrid[x][y]["Connections"]["Up"] = True

        elif y + 1 < Rows and not MazeGrid[x][y + 1]["Visited"] and MazeGrid[x][y + 1] == NextCell: # Down

            CellGrid[x * 2][y * 2 + 1]["IsWall"] = False 
            MazeGrid[x][y]["Connections"]["Down"] = True   

        elif x + 1 < Cols and not MazeGrid[x + 1][y]["Visited"] and MazeGrid[x + 1][y] == NextCell: # Right

            CellGrid[x * 2 + 1][y * 2]["IsWall"] = False
            MazeGrid[x][y]["Connections"]["Right"] = True
        
        elif x - 1 != 0 and not MazeGrid[x - 1][y]["Visited"] and MazeGrid[x - 1][y] == NextCell: # Left

            CellGrid[x * 2 - 1][y * 2]["IsWall"] = False    
            MazeGrid[x][y]["Connections"]["Left"] = True

    else:
        
        del Stack[len(Stack)] 

def SearchGrid(MazeGrid, CellGrid, Rows, Cols):

    if not Stack or len(Stack) == 0:
        return False

    CurrentCell = Stack[len(Stack)]
    CurrentCell["Visited"] = True

    x = CurrentCell["X"]
    y = CurrentCell["Y"]

    CheckNeighbours(MazeGrid, CellGrid, x, y, Rows, Cols)

    return True

def Create(MazeGrid, CellGrid, Rows, Cols):

    # Setup

    Stack[1] = MazeGrid[1][1]

    # Entrance And Exit 

    CellGrid[2][1]["IsWall"] = False
    CellGrid[Cols - 1][Rows]["IsWall"] = False

    # Main Loop

    while True: # Seems Like It Crashes, It Does Not 
        if SearchGrid(MazeGrid, CellGrid, Rows, Cols) == False: break

    