# Maze Mode File
# image from
# https://github.com/ZiadElGafy/Fireboy-And-Watergirl/tree/master/assets/graphics
from cmu_112_graphics import *
import random
import maze as mz
NORTH = (0,-1)
SOUTH = (0,1)
WEST = (-1,0)
EAST = (1,0)

def manhattanDistance(ax,ay,bx,by):
    return abs(ax-bx) + abs(ay-by)

def findShortestMD(ax,ay,positionList): # best template to find nearest target
    bestx,besty = 1000,1000
    bestMD = 1000
    for bx,by in positionList:
        currMD = manhattanDistance(ax,ay,bx,by)
        if currMD < bestMD:
            bestMD = currMD
            bestx,besty = bx,by
    return bestx,besty


class Char(object):
    def __init__(self,px,py,element): # position expressed as grid, color decides image
        self.px = px
        self.py = py
        self.element = element
        self.image = ''
        self.doorImage = ''
        self.gemImage = ''
        self.gemPosition = []
        self.doorPosition = []
        self.doorOpen = False
        self.path = []
        self.hint = 3
        self.hintOn = False
        self.hintCount = 0
        self.win = False
    
    def mazeAppRun(self,app): # put under appStarted
        if self.element == 'fire':
            self.image = app.scaleImage(app.loadImage('fireBoy.png'),0.3)
            self.doorImage = app.scaleImage(app.loadImage('firedoormaze.png'),0.3)
            self.gemImage = app.scaleImage(app.loadImage('redGem.png'),0.4)
        else:
            self.image = app.scaleImage(app.loadImage('waterGirl.png'),0.3)
            self.doorImage = app.scaleImage(app.loadImage('waterdoormaze.png'),0.3)
            self.gemImage = app.scaleImage(app.loadImage('blueGem.png'),0.4)

        ### random gem generation ###
        randEmpty = []
        for i in range(app.maze.row):
            for j in range(app.maze.col):
                if (manhattanDistance(1,1,i,j) > 8 and i > 1 and j > 1 
                    and i < app.maze.row-1 and j < app.maze.col-1 and app.maze.maze[i][j] != 1):
                    randEmpty.append((i,j))
        while len(self.gemPosition) < 5: # could be changed according to difficulty
            g = random.choice(randEmpty)
            while g in self.gemPosition:
                g = random.choice(randEmpty)
            self.gemPosition.append(g)
        
        ### random door generation ###
        randDoor = []
        for i in range(app.maze.row):
            for j in range(app.maze.col):
                if (i == 0 or i == app.maze.row-1) or (j == 0 or j == app.maze.col-1):
                    if self.element == 'fire':
                        if manhattanDistance(1,1,i,j) > 14:
                            randDoor.append((i,j))
                    elif self.element == 'water':
                        if manhattanDistance(1,app.maze.col-1,i,j) > 14:
                            randDoor.append((i,j))
        dx,dy = random.choice(randDoor)
        while isNotValid(app,dx,dy):
            dx,dy = random.choice(randDoor) # make sure the door can be reached
        self.doorPosition.append((dx,dy))
        app.maze.maze[dx][dy] = 9 # represent door

    def mazeCharKeyPressed(self,app,event): # put under keyPressed
        if self.element == 'fire':
            dx,dy = 0,0
            if event.key == 'Up':
                dx,dy = NORTH
            elif event.key == 'Down':
                dx,dy = SOUTH
            elif event.key == 'Left':
                dx,dy = WEST
            elif event.key == 'Right':
                dx,dy = EAST
            row = self.px + dx
            col = self.py + dy
            if not(row < 0 or row > app.maze.row-1 or 
                    col < 0 or col > app.maze.col - 1 or app.maze.maze[row][col] == 1):
                    self.px = row
                    self.py = col
            if event.key == '1' and self.hint > 0: # draw hint line
                self.hintOn = True
        if self.element == 'water':
            dx,dy = 0,0
            if event.key == 'w':
                dx,dy = NORTH
            elif event.key == 's':
                dx,dy = SOUTH
            elif event.key == 'a':
                dx,dy = WEST
            elif event.key == 'd':
                dx,dy = EAST
            row = self.px + dx
            col = self.py + dy
            if not(row < 0 or row > app.maze.row-1 or 
                    col < 0 or col > app.maze.col - 1 or app.maze.maze[row][col] ==1):
                    self.px = row
                    self.py = col
            if event.key == 'h' and self.hint > 0:
                self.hintOn = True
    
    def eatGem(self):
        if len(self.gemPosition) == 0:
            dx,dy = self.doorPosition[0]
            self.doorOpen = True
            if self.px ==dx and self.py == dy:
                self.win = True
        else:
            for gx, gy in self.gemPosition:
                if gx == self.px and gy == self.py:
                    self.gemPosition.remove((gx,gy))
            
    def hintCounter(self,app):
        if self.hintOn:
            self.hintCount += 1
            if self.hintCount > 30:
                self.hintCount = 0
                self.hintOn =False
                self.hint -= 1

    def placeChar(self,app):
        for i in range(app.maze.row):
            for j in range(app.maze.col):
                if self.element == 'fire':
                    if app.maze.maze[i][j] == 5 and (i != self.px or j != self.py):
                    # occupied by fireBoy but char not on this spot
                        app.maze.maze[i][j] = 0
                    elif app.maze.maze[i][j] == 0 and i == self.px and j == self.py:
                        app.maze.maze[i][j] = 5 # occupuied by fireBoy (5)
                elif self.element == 'water':
                    if app.maze.maze[i][j] == 8 and (i != self.px or j != self.py):
                    # occupied by waterGirl but char not on this spot
                        app.maze.maze[i][j] = 0
                    elif app.maze.maze[i][j] == 0 and i == self.px and j == self.py:
                        app.maze.maze[i][j] = 8 # occupuied by waterGirl (8)

    def findTarget(self):
        if self.doorOpen == False:
            return findShortestMD(self.px,self.py,self.gemPosition)
        else:
            dx,dy = self.doorPosition[0]
            if dx ==0:
                dx = 1
            elif dx == self.maze.row-1:
                dx = self.maze.row-2
            elif dy == 0:
                dy = 1
            elif dy == self.maze.col-1:
                dy = self.maze.col-2
            return dx,dy

    def solvePath(self,app):
        startRow = self.px
        startCol = self.py
        endRow,endCol = self.findTarget()
        self.path = mz.solveMaze(app,startRow,startCol,endRow,endCol)

def isNotValid(app,dx,dy): # helper that tells if the door is not valid
    if dx == 0:
        if app.maze.maze[dx+1][dy] == 1: return True # not valid
    elif dx == app.maze.col-1:
        if app.maze.maze[dx-1][dy] == 1: return True
    elif dy == 0:
        if app.maze.maze[dx][dy+1] == 1: return True
    elif dy == app.maze.row-1 :
        if app.maze.maze[dx][dy-1] == 1: return True
    elif dx==dy or (dx==app.maze.row-1 and dy == 0) or (dy == app.maze.col-1 and dx == 0):
        return True # on the corner
    return False

    

        
            
        

