from threading import current_thread
from algorithms.astar import a_star
from components.buttons import Button
from components.side_buttons import SideButton
import pygame
import math

pygame.init()
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH + 200, WIDTH + 130))
pygame.display.set_caption("Path Finding Algorithms")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
SLATEBLUE = (106, 90, 205)
SPRINGGREEN = (0, 250, 154)
CRIMSON = (220, 20, 60)
KHAKI = (240, 230, 140)
ORANGERED = (255, 69, 0) 
CORAL = (255, 127, 80)

#(self, color, x, y, width, height, text='')
barrierButton = Button((209, 194, 255), 10, 810, 150, 100, 'Walls')
startButton = Button(ORANGE, 170, 810, 150, 100, 'Start Position')
endButton = Button(TURQUOISE, 330, 810, 150, 100, 'End Position')
beginButton = Button(GREEN, 490, 810, 150, 100, 'Begin Pathfinding')
clearButton = Button(YELLOW, 650, 810, 150, 100, 'Clear Grid')
#Side buttons
aStarButton = SideButton(WHITE, 801, 123, 198, 55, 'A* algorithm', True)
dijkstraButton = SideButton(WHITE, 801, 178, 198, 55, 'Dijkstra algorithm')
bellmanFordButton = SideButton(WHITE, 801, 233, 198, 55, 'Bellman Ford algorithm')


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
    win.blit(textAlgorithms, (855, 70))  
  


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
                if pos[0] <= 800 and pos[1] <= 800:
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
                if pos[0] <= 800 and pos[1] <= 800:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

    pygame.quit()

main(WIN, WIDTH)