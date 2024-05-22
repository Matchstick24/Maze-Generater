import pygame
import MazeGenerater
import DijkstraPathfinding
import AstarPathfinding

pygame.init()
pygame.display.set_caption("Maze Generator")

screen_width, screen_height = 1210, 610
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

CellSize = 20
CellOffset = 0
CameraX, CameraY = 0, 0
CameraSpeed = 0.5

Rows = 100 * 2 + 1
Cols = 100 * 2 + 1

CellGrid = {}
MazeGrid = {}
OrginalCellSize = CellSize

for x in range(1, Cols + 1): # For The Cell Grid 

        CellGrid[x] = {}

        for y in range(1,  Rows + 1):

            CellGrid[x][y] = {

                "IsWall" : True,
                "X" : x,
                "Y" : y, 

            }

################################################

IsX = False # Used Later

for x in range(1, Cols + 1): # For The Maze Grid 

        if IsX:

            MazeGrid[int(x / 2)] = {}
            IsY = False # Used Later

            for y in range(1, Rows + 1):
                    
                    if IsY:

                        MazeGrid[int(x / 2)][int(y / 2)] = {

                            "X" : int(x / 2),
                            "Y" : int(y / 2),
                            "Visited" : False,

                            # Dijkstra Pathfinding
				
                            # "Distance" : math.inf,
                            # "Explored" : False,
                            # "Parent" : None,

                            # "Connections" : {

                            #     "Up" : False,
                            #     "Down" : False,
                            #     "Right" : False,
                            #     "Left" : False,

                            # },

                            # Astar Pathfinding
				
                            "Gcost" : 0,
                            "Hcost" : 0,
                            "Fcost" : 0,
                            "Parent" : None,
                            "Open" : False,
                            "Closed" : False,

                            "Connections" : {

                                "Up" : False,
                                "Down" : False,
                                "Right" : False,
                                "Left" : False,

                            },
                        }

                        CellGrid[x][y]["IsWall"] = False

                    IsY = not IsY

        IsX = not IsX

MazeGenerater.Create(MazeGrid, CellGrid, Rows, Cols)
maze_surface = pygame.Surface((Cols * CellSize, Rows * CellSize,))
Waypoints = AstarPathfinding.FindPath(MazeGrid, int(Rows / 2), int(Cols / 2), {"X" : 1, "Y" : 1}, {"X" : int(Cols / 2), "Y" : int(Rows / 2)})

def UpdateScreen():

    maze_surface.fill((255,255,255))

    for x in range(1, Cols + 1):
        for y in range(1, Rows + 1):

            if CellGrid[x][y]["IsWall"]:

                Cell = pygame.Rect((x - 1) * CellSize + int(CameraX * (CameraSpeed * CellSize)), (y - 1) * CellSize + int(CameraY * (CameraSpeed * CellSize)), CellSize - CellOffset, CellSize - CellOffset)
                pygame.draw.rect(maze_surface, (0, 0, 0), Cell)

    for Waypoint in range(1, len(Waypoints) + 1):

        x = Waypoints[Waypoint]["X"]
        y = Waypoints[Waypoint]["Y"]

        Cell = pygame.Rect((x - 1) * CellSize + int(CameraX * (CameraSpeed * CellSize)), (y - 1) * CellSize + int(CameraY * (CameraSpeed * CellSize)), CellSize - CellOffset, CellSize - CellOffset)
        pygame.draw.rect(maze_surface, (200, 0, 255), Cell)

    screen.blit(maze_surface, (0, 0))

    pygame.display.flip()

while running:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if keys[pygame.K_o]:
                CellSize -= 1
            elif keys[pygame.K_i]:
                CellSize += 1
            elif keys[pygame.K_p]:
                CellSize = OrginalCellSize
                CameraX, CameraY = 0, 0

            if CellSize < 1:
                CellSize = 1
            elif CellSize > 100 :
                CellSize = 100

    if keys[pygame.K_x]:
        running = False
    
    if keys[pygame.K_w]:
        CameraY += 1
    if keys[pygame.K_s]:
        CameraY -= 1

    if keys[pygame.K_d]:
        CameraX -= 1
    if keys[pygame.K_a]:
        CameraX += 1

    UpdateScreen()
    dt = clock.tick(300)

pygame.quit()