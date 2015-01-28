from __future__ import print_function
import pygame, sys, random, time
from pygame.locals import *

def blankCell():        # Returns a blank list 
    bCell = [[" "]*CELLS for i in range(CELLS)]
    return bCell

def highlight(block):       # Highlights the block
    color = random.choice([BLACK, RED, SILVER, BLUE, GREEN])        # Randomly chooses a color to highlight the block
    pygame.draw.rect(windowSurface, color, (block.left-1, block.top-1, block.width+2, block.height+2), 1)
            
def makePattern(cell):      # Draws the cell pattern on the screen 
    HIGHLIGHT = False
    while True:
        windowSurface.fill(WHITE)
        pygame.draw.rect(windowSurface, GRAY, (0, len(cell[0])*CELLSIZE+2*MARGIN, len(cell)*CELLSIZE+2*MARGIN, 30))
        fontObj = pygame.font.SysFont("Comic Sans MS", 15)
        text = fontObj.render(("Alive: %s       Dead: %s" % deadAlive(cell)), True, BLACK)
        textRect = text.get_rect()
        textRect.center = ((len(cell)*CELLSIZE+MARGIN*2)/2, 15 + (len(cell[0])*CELLSIZE+MARGIN*2))          # 15 because the height of rectangle is 30 pixel
        windowSurface.blit(text, textRect)
        drawCell(cell)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == ord("r"):
                    cell = blankCell()
                if event.key == K_SPACE:
                    main(cell)
            if event.type == MOUSEMOTION:
                x, y = event.pos[0], event.pos[1]
                for i in range(len(cell)):
                    for j in range(len(cell[i])):
                        tempCell = pygame.Rect(i*CELLSIZE+MARGIN, j*CELLSIZE+MARGIN, CELLSIZE-MARGIN, CELLSIZE-MARGIN) 
                        if tempCell.colliderect((x, y, 0, 0)):
                            HIGHLIGHT = True
                            block = tempCell
            if event.type == MOUSEBUTTONDOWN:
                tCell = cell[:]
                x, y = event.pos[0], event.pos[1]
                for i in range(len(tCell)):
                    for j in range(len(tCell[i])):
                        tempCell = pygame.Rect(i*CELLSIZE+MARGIN, j*CELLSIZE+MARGIN, CELLSIZE-MARGIN, CELLSIZE-MARGIN) 
                        if tempCell.colliderect((x, y, 0, 0)):
                            if cell[i][j] == "o": cell[i][j] = " "
                            else: cell[i][j] = "o"
        if HIGHLIGHT:                
            highlight(block)
        pygame.display.update()
        fpsClock.tick(FPS)

def main(cell):
    while True:
        windowSurface.fill(WHITE)
        pygame.draw.rect(windowSurface, GRAY, (0, len(cell[0])*CELLSIZE+2*MARGIN, len(cell)*CELLSIZE+2*MARGIN, 30))
        drawCell(cell)                              # draws board in its current state
        aCells = getAliveCells(cell)        # Alive cells
        dCells = getDeadCells(aCells)   # Dead Cells
        for x, y in aCells: cell[x][y] = "o"                            # sets alive cells
        for x, y in dCells: cell[x][y] = " "                            # sets dead cells
        fontObj = pygame.font.SysFont("Comic Sans MS", 15)
        text = fontObj.render(("Alive: %s       Dead: %s" % deadAlive(cell)), True, BLACK)
        textRect = text.get_rect()
        textRect.center = ((len(cell)*CELLSIZE+MARGIN*2)/2, 15 + (len(cell[0])*CELLSIZE+MARGIN*2))          # 15 because the height of rectangle is 30 pixel
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == ord("r"):
                    cell = blankCell()
                    makePattern(cell)
                if event.key == K_SPACE:
                    makePattern(cell)
        windowSurface.blit(text, textRect)
        pygame.display.update()
        fpsClock.tick(FPS)

def deadAlive(cell):        # Returns current number of dead and alive cells
    nAlive = 0
    nDead = 0
    for row in cell:
        nAlive += row.count("o")
        nDead += row.count(" ")
    return nAlive, nDead

def alive(x, y):    #draws alive cells
    color = random.choice([GREEN, RED, BLUE])       # randomize the color for alive cell
    pygame.draw.rect(windowSurface, color, (x+MARGIN, y+MARGIN, CELLSIZE-MARGIN, CELLSIZE-MARGIN))

def dead(x, y):     #draws dead cells
    pygame.draw.rect(windowSurface, WHITE, (x, y, CELLSIZE, CELLSIZE))

def drawCell(cell):    # Prints the whole cell
    top = 0
    left = 0
    for i in range(len(cell)):
        left = i*CELLSIZE
        for j in range(len(cell[i])):
            top = j*CELLSIZE
            if cell[i][j] == "o":
                alive(left, top)
            if cell[i][j] == " ":
                dead(left, top)

def getAliveCells(cell):    # Returns alive cells' coordinates
    aliveCells = []
    for i in range(len(cell)):          # This code and the code below checks each and every space in the pattern. from cell[0][0] to cell[n][n] where n = len(cell) -1
        for j in range(len(cell[i])):
            alive = 0                   # Sets number of alive cell to 0 before checking the cell
            for dx, dy in [[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1]]:  # [1,0], [1,-1],. . . . .[1, 1] are the directions. See below the program to know how direction works.
                x = i + dx
                y = j + dy
                if 0 <= x <= (len(cell) - 1) and 0 <= y <= (len(cell[i]) - 1): # If within board and I don't know why but the program runs only if I subtract 2 from y. It is still a mystery to me.
                    if cell[x][y] == "o":   # If the cell in a direction is alive. 
                        alive += 1
            if alive == 2 or alive == 3:    # If the total number of alive cells around at last is 2 or 3
                aliveCells.append([i, j])   # Add the current coordinate to the list aliveCells to be kept alive in next step
    return aliveCells

def getDeadCells(aCells):     # Returns dead cells' coordinates
    deadCells = []
    for i in range(len(cell)):          # This function is pretty similat to getAliveCells(cell) one. Just the difference is that this function tells which cell should be dead in next step.
        for j in range(len(cell[i])):
            if [i, j] not in aCells:        
                deadCells.append([i, j])
    return deadCells

# Functions end and program starts here
pygame.init()

FPS = 12
fpsClock = pygame.time.Clock()
CELLSIZE = 9     # Size of each cell
MARGIN = 2       # Margin among cells
CELLS = 30          # Number of rows or columns

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255, 100)
GRAY = (128, 128, 128, 10)
SILVER = (192, 192, 192, 10)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Get a blank board of cells
cell = blankCell()

# Set up the window surface and title
windowSurface = pygame.display.set_mode((len(cell)*CELLSIZE+2*MARGIN, len(cell[0])*CELLSIZE+2*MARGIN+30))           # 30 is to make a rectangle of height 30 pixel at bottom to show number of alive and dead cells 
pygame.display.set_caption("Conway's Game of Life")

# Set up the background music
pygame.mixer.music.load("Firefly - Owl City.mp3")
pygame.mixer.music.play(-1, 0.0)

# Show initial instruction about the program
windowSurface.fill(BLACK)
font = pygame.font.SysFont("Comic Sans MS", 12)
textObj1 = font.render("Click on screen to make your initial pattern.", True, WHITE)
textRect1 = textObj1.get_rect()
textRect1.centerx = windowSurface.get_rect().centerx
textRect1.centery = windowSurface.get_rect().centery-30
textObj2 = font.render("Press 'R' to reset.", True, WHITE)
textRect2 = textObj2.get_rect()
textRect2.centerx = windowSurface.get_rect().centerx
textRect2.centery = windowSurface.get_rect().centery-10
textObj3 = font.render("Press SPACE key to start or pause.", True, WHITE)
textRect3 = textObj3.get_rect()
textRect3.centerx = windowSurface.get_rect().centerx
textRect3.centery = windowSurface.get_rect().centery+10
# Write both text objects on the screen
windowSurface.blit(textObj1, textRect1)
windowSurface.blit(textObj2, textRect2)
windowSurface.blit(textObj3, textRect3)
# Display the updated windowSurface
pygame.display.update()
time.sleep(4)
# Allows user to make his/her own pattern on the screen
makePattern(cell)
