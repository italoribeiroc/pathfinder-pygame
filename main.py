from threading import current_thread
from algorithms.astar import a_star
#from algorithms.Dijkstra import dijkstra
from assets.colors import *
from components.buttons import Button
from components.side_buttons import SideButton
import pygame
import math

pygame.init()
SCREEN_HEIGHT = pygame.display.Info().current_h
DISPLAYS = [(1024,576),(1152,648),(1280,720),(1600,900),(1920,1080),(2560,1440)] 
i = 0
while DISPLAYS[i][1] < SCREEN_HEIGHT:
    i+=1
SCREEN_WIDTH, SCREEN_HEIGHT = DISPLAYS[i]
WIDTH = (800*SCREEN_HEIGHT)//1080
RIGHT_WIN = (130*SCREEN_HEIGHT)//1080
BOTTOM_WIN = (200*SCREEN_WIDTH)//1920
WIN = pygame.display.set_mode((WIDTH + BOTTOM_WIN, WIDTH + RIGHT_WIN), flags = pygame.SCALED)
pygame.display.set_caption("Path Finding Algorithms")

BUTTON_WIDTH = (150*SCREEN_WIDTH)//1920
BUTTON_HEIGHT = (100*SCREEN_HEIGHT)//1080
BUTTON_POS_X =  (10*SCREEN_WIDTH)//1920
BUTTON_POS_Y = (810*SCREEN_HEIGHT)//1080
BUTTON_SPACE = (160*SCREEN_WIDTH)//1920
print(SCREEN_WIDTH)
#(self, color, x, y, width, height, text='')
barrierButton = Button((209, 194, 255), BUTTON_POS_X, BUTTON_POS_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 'Walls')
startButton = Button(ORANGE, BUTTON_POS_X+BUTTON_SPACE, BUTTON_POS_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 'Start Position')
endButton = Button(TURQUOISE, BUTTON_POS_X+BUTTON_SPACE*2, BUTTON_POS_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 'End Position')
beginButton = Button(GREEN, BUTTON_POS_X+BUTTON_SPACE*3, BUTTON_POS_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 'Begin Pathfinding')
clearButton = Button(YELLOW, BUTTON_POS_X+BUTTON_SPACE*4, BUTTON_POS_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 'Clear Grid')
#Side buttons

SBUTTON_WIDTH = (198*SCREEN_WIDTH)//1920
SBUTTON_HEIGHT = (55*SCREEN_HEIGHT)//1080
SBUTTON_POS_X =  (801*SCREEN_WIDTH)//1920
SBUTTON_POS_Y = (100*SCREEN_HEIGHT)//1080
SBUTTON_SPACE = (55*SCREEN_WIDTH)//1920
aStarButton = SideButton(WHITE, SBUTTON_POS_X, SBUTTON_POS_Y, SBUTTON_WIDTH, SBUTTON_HEIGHT, 'A* algorithm', True)
dijkstraButton = SideButton(WHITE, SBUTTON_POS_X, SBUTTON_POS_Y+SBUTTON_HEIGHT, SBUTTON_WIDTH, SBUTTON_HEIGHT, 'Dijkstra algorithm')
bellmanFordButton = SideButton(WHITE, SBUTTON_POS_X, SBUTTON_POS_Y+SBUTTON_HEIGHT+SBUTTON_HEIGHT, SBUTTON_WIDTH, SBUTTON_HEIGHT, 'Bellman Ford algorithm')


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col 
        self.x = row * width
        self.y = col* width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_close(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row ][self.col + 1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            if i == 0 or i == rows-1 or j == 0 or j == rows-1:
                node.make_barrier()
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def write_text(win):
    font = pygame.font.SysFont('comicsans', 22)
    pygame.font.init()
    textAlgorithms = font.render('Algorithms', 1, BLACK)
    win.blit(textAlgorithms, ((855*SCREEN_WIDTH)//1920, (40*SCREEN_HEIGHT)//1080))  
  


def draw(win, grid, rows, width):
    win.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)

    barrierButton.draw(win, GREY)
    startButton.draw(win, GREY)
    endButton.draw(win, GREY)
    beginButton.draw(win, GREY)
    clearButton.draw(win, GREY)
    aStarButton.draw(win, GREY)
    dijkstraButton.draw(win, GREY)
    bellmanFordButton.draw(win, GREY)

    write_text(win)

    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap 

    return row, col

def disable_buttons(button: Button):
    state = button.active
    barrierButton.active = False
    startButton.active = False
    endButton.active = False
    beginButton.active = False
    clearButton.active = False
    button.active = True if not state else False

def disable_algorithms(button: Button):
    aStarButton.active = False
    dijkstraButton.active = False
    bellmanFordButton.active = False
    button.active = True
    
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None
    run = True
    # beginActivated = False 

    while run:
        draw(win, grid, ROWS, width)
        if beginButton.active and start and end:
            for row in grid:
                for node in row:
                    node.update_neighbors(grid)
            if (aStarButton.active):
                a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
            elif (dijkstraButton.active):
                pass
                #dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
            elif (bellmanFordButton):
                pass
            beginButton.active = False
            
            # beginActivated = True
        if clearButton.active:
            start = None
            end = None
            grid = make_grid(ROWS, width)
            clearButton.active = False
            # beginActivated = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                if pos[0] <= WIDTH and pos[1] <= WIDTH:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    if startButton.active and not start and node != end:
                        start = node
                        start.make_start()
                        startButton.active = False
                    if endButton.active and not end and node != start:
                        end = node
                        end.make_end()
                        endButton.active = False
                    if barrierButton.active and node != end and node != start:
                        node.make_barrier()

                #Bottoms buttons click
                elif barrierButton.isOver(pos):
                    disable_buttons(barrierButton)
                elif startButton.isOver(pos):
                    disable_buttons(startButton)
                elif endButton.isOver(pos):
                    disable_buttons(endButton)
                elif beginButton.isOver(pos):
                    disable_buttons(beginButton)
                elif clearButton.isOver(pos):
                    disable_buttons(clearButton)

                #Side Buttons click
                elif aStarButton.isOver(pos):
                    disable_algorithms(aStarButton)
                elif dijkstraButton.isOver(pos):
                    disable_algorithms(dijkstraButton)
                elif bellmanFordButton.isOver(pos):
                    disable_algorithms(bellmanFordButton)
                


            # elif pygame.mouse.get_pressed()[2] and not beginActivated: # RIGHT
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                if pos[0] <= WIDTH and pos[1] <= WIDTH:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

    pygame.quit()

main(WIN, WIDTH)