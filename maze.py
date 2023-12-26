# a maze generation algorithm using Prim algorithm

# tile image 
# https://www.pinterest.com/pin/534521049524541611/
# logic of prim algorithm learned by watching vedio:
# https://www.bilibili.com/video/BV1uf4y1s7ch?from=search
# &seid=2143239820952882822&spm_id_from=333.337.0.0

import random
from cmu_112_graphics import *
NORTH = (0,-1)
SOUTH = (0,1)
WEST = (-1,0)
EAST = (1,0)


class Maze(object):
    # maze generation based on prim algorithm or the logic of minimum spanning tree
    def __init__(self,row,col):
        self.row = row
        self.col = col # col and row has to be odd
        self.maze = [[1 for i in range(row)] for j in range(col)]
        self.forest = []
        self.vertices = []
        self.start = [1,1]
        self.end = [row-2,col-2]
        for i in range(1,row,2):
            for j in range(1,col,2):
                self.maze[i][j] = 0
                self.forest.append([[i,j]])
                self.vertices.append([i,j])
        while len(self.forest) > 1:
            for point in self.vertices:
                self.breakWall(point)

    # after planting trees, loop through each tree and try to connect and merge 
    # all trees into one single tree
    def breakWall(self,point):
        direction = [1,2,3,4]
        startTree = []
        connectedTree = []
        tar = []
        for tree in self.forest:
            if point in tree: # find the tree the point belongs to
                startTree = tree
                break
        if len(self.forest) == 1: # only one tree, completed
            return
        px,py = point[0],point[1]
        if px < 2 or [px-2,py] in startTree: # can't go up
            direction.remove(1)
        if py< 2 or [px,py-2] in startTree: # can't go left
            direction.remove(2)
        if px>self.row-3 or [px+2,py] in startTree: # can't go down
            direction.remove(3)
        if py>self.col-3 or [px,py+2] in startTree: # can't go right
            direction.remove(4)
        dir = random.choice(direction)
        if dir == 1:
            self.maze[px-1][py] = 0 # break the wall
            tar = [px-2,py]
        elif dir == 2:
            self.maze[px][py-1] = 0 
            tar = [px,py-2]
        elif dir == 3:
            self.maze[px+1][py] = 0
            tar = [px+2,py]
        elif dir == 4:
            self.maze[px][py+1] = 0
            tar = [px,py+2]
        for tree in self.forest:
            if tar in tree:
                connectedTree = tree
                break
        startTree.extend(connectedTree)
        self.forest.remove(connectedTree)


def createNewMaze(app):
    if app.mazeLevel == 'easy':
        app.maze = Maze(19,19)
    if app.mazeLevel == 'medium':
        app.maze = Maze(25,25) # maze instance
    if app.mazeLevel == 'hard':
        app.maze = Maze(31,31)


# checks if a direction is valid
def isValid(maze,row,col,direction):
    mrow,mcol = len(maze),len(maze[0])
    if row < 1 or row >= mrow-1 or col < 1 or col >= mcol - 1:
        return False
    dx,dy = direction
    x = row + dx
    y = col + dy
    if maze[x][y] == 1:
        return False
    else:
        return True # zero valid and 1 not valid


# backtracking template
def solveMaze(app,startRow,startCol,endRow,endCol):
    visited = []
    m = app.maze.maze
    end = (endRow,endCol)
    def solve(row,col):
        if (row,col) in visited: return False
        visited.append((row,col))
        if (row,col) == end: return True
        for dx,dy in [NORTH,SOUTH,WEST,EAST]:
            if isValid(m,row,col,(dx,dy)):
                nextx = row + dx
                nexty = col + dy
                if solve(nextx,nexty): return True
        visited.remove((row,col))
        return False
    return visited if solve(startRow,startCol) else None


# get the real coordinate of the grid
def getGridPosition(app,i,j):
    gridWidth = 700/app.maze.row
    x0 = 450 + i*gridWidth
    y0 = 50+j*gridWidth
    return x0,y0


def drawMaze(app,canvas):
    for i in range(app.maze.row):
        for j in range(app.maze.col): # drw maze map and character
            if app.maze.maze[i][j] == 1:
                x,y = getGridPosition(app,i,j)
                canvas.create_image(x,y,image = app.tileImage)
            elif app.maze.maze[i][j] == 5:
                x,y = getGridPosition(app,i,j)
                canvas.create_image(x,y,image = app.mazeFire.image)
            elif app.maze.maze[i][j] == 8:
                x,y = getGridPosition(app,i,j)
                canvas.create_image(x,y,image = app.mazeWater.image)
    # draws the suggested path(hint)
    if app.mazeFire.hintOn:
        if len(app.mazeFire.path) > 0:
            for x,y in app.mazeFire.path:
                cx,cy = getGridPosition(app,x,y)
                canvas.create_oval(cx-4,cy-4,cx+4,cy+4,fill = 'orangered')
    elif app.mazeWater.hintOn:
        if len(app.mazeWater.path) > 0:
            for x,y in app.mazeWater.path:
                cx,cy = getGridPosition(app,x,y)
                canvas.create_oval(cx-4,cy-4,cx+4,cy+4,fill = 'cyan')
    
    # draws the door
    for x,y in app.mazeFire.doorPosition:
        cx,cy = getGridPosition(app,x,y)
        canvas.create_image(cx,cy,image = app.mazeFire.doorImage)
    for x,y in app.mazeWater.doorPosition:
        cx,cy = getGridPosition(app,x,y)
        canvas.create_image(cx,cy,image = app.mazeWater.doorImage)
    # draws gems
    for x,y in app.mazeFire.gemPosition:
        cx,cy = getGridPosition(app,x,y)
        canvas.create_image(cx,cy,image = app.mazeFire.gemImage)
    for x,y in app.mazeWater.gemPosition:
        cx,cy = getGridPosition(app,x,y)
        canvas.create_image(cx,cy,image = app.mazeWater.gemImage)
    # draws game win info
    if app.mazeWater.win == True:
        canvas.create_text(600,350,text = 'WaterGirl WINS :)',font ='Algerian 50 bold',fill = 'aqua')
    if app.mazeFire.win == True:
        canvas.create_text(600,350,text = 'FireBoy WINS :)',font = 'Algerian 50 bold',fill='orangered')
    # draws general text
    canvas.create_text(150,20,text = 'press "r" to change map!',font = 'Arial 16 bold',fill = 'yellow')
    canvas.create_text(150,40,text = '{:>63}'.format('press "m/n" to change different levels!')
                                ,font = 'Arial 16 bold',fill = 'yellow')
    canvas.create_text(150,60,text = '{:>53}'.format('press "p" to turn on/off AI mode!'),font = 'Arial 16 bold',fill = 'yellow')    
    canvas.create_image(150,200,image = app.mazeFire.displayImage)
    canvas.create_image(150,500,image = app.mazeWater.displayImage)
    canvas.create_text(300,200,text = 'FireBoy',font = 'Arial 23 bold',fill = 'orangered')
    canvas.create_text(300,500,text = 'WaterGirl',font ='Arial 23 bold',fill = 'aqua')
    canvas.create_text(200,270,text = '{:<20}'.format(f'Gems left: {len(app.mazeFire.gemPosition)}')  ,
                            font = 'Arial 25 bold',fill = 'orangered')
    canvas.create_text(200,570,text = '{:<20}'.format(f'Gems left: {len(app.mazeWater.gemPosition)}'),
                            font = 'Arial 25 bold',fill = 'aqua')
    canvas.create_text(200,330,text = f'hint left: {app.mazeFire.hint}\n press 1 for hint',
                            font = 'Arial 25 bold',fill='orangered')
    canvas.create_text(200,630,text = f'hint left: {app.mazeWater.hint}\n press h for hint',
                            font = 'Arial 25 bold',fill='aqua')
    if app.mazeFire.doorOpen:
        canvas.create_text(285,220,text='(Door is Open!)',font = 'Arial 15 bold',
                            fill = 'orangered' )
    if app.mazeWater.doorOpen:
        canvas.create_text(285,525,text='(Door is Open!)',font = 'Arial 15 bold',
                            fill = 'aqua' )
    if app.AImode:
        canvas.create_text(245,400,
        text = '{:<50}'.format('you can select your AI strength\n by pressing 2,3,4;with 4 the strongest AI')
                            ,font = 'Arial 15 bold',fill = 'yellow' )
        canvas.create_text(245,430,
        text='{:<50}'.format('you are now controlling WaterGirl against AI!'),
                            font = 'Arial 15 bold',
                            fill = 'yellow' )


###########################################
## character class
###########################################

# distance used to calculate when generating gems and doors
def manhattanDistance(ax,ay,bx,by):
    return abs(ax-bx) + abs(ay-by)

def findShortestMD(ax,ay,positionList): # best template to find nearest target
    bestx,besty = 100,100
    bestMD = 100
    for bx,by in positionList:
        currMD = manhattanDistance(ax,ay,bx,by)
        if currMD < bestMD:
            bestMD = currMD
            bestx,besty = bx,by
    return bestx,besty

# character class in maze
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
            if app.mazeLevel == 'medium':
                self.image = ImageTk.PhotoImage(app.scaleImage(app.loadImage('fireBoy.png'),0.3))
                self.displayImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('fireBoy.png'),1.3))
                self.doorImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('firedoormaze.png'),0.3))
                self.gemImage = ImageTk.PhotoImage((app.scaleImage(app.loadImage('redGem.png'),0.4)))
            elif app.mazeLevel == 'easy':
                self.image = ImageTk.PhotoImage(app.scaleImage(app.loadImage('fireBoy.png'),0.5))
                self.displayImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('fireBoy.png'),1.3))
                self.doorImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('firedoormaze.png'),0.4))
                self.gemImage = ImageTk.PhotoImage((app.scaleImage(app.loadImage('redGem.png'),0.6)))
            elif app.mazeLevel == 'hard':
                self.image = ImageTk.PhotoImage(app.scaleImage(app.loadImage('fireBoy.png'),0.25))
                self.displayImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('fireBoy.png'),1.3))
                self.doorImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('firedoormaze.png'),0.25))
                self.gemImage = ImageTk.PhotoImage((app.scaleImage(app.loadImage('redGem.png'),0.35)))

        else:
            if app.mazeLevel == 'medium':
                self.image = ImageTk.PhotoImage(app.scaleImage(app.loadImage('waterGirl.png'),0.3))
                self.displayImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('waterGirl.png'),1.3))
                self.doorImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('waterdoormaze.png'),0.3))
                self.gemImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('blueGem.png'),0.4))
            elif app.mazeLevel == 'easy':
                self.image = ImageTk.PhotoImage(app.scaleImage(app.loadImage('waterGirl.png'),0.5))
                self.displayImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('waterGirl.png'),1.3))
                self.doorImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('waterdoormaze.png'),0.4))
                self.gemImage = ImageTk.PhotoImage((app.scaleImage(app.loadImage('blueGem.png'),0.6)))
            elif app.mazeLevel == 'hard':
                self.image = ImageTk.PhotoImage(app.scaleImage(app.loadImage('waterGirl.png'),0.25))
                self.displayImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('waterGirl.png'),1.3))
                self.doorImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('waterdoormaze.png'),0.25))
                self.gemImage = ImageTk.PhotoImage((app.scaleImage(app.loadImage('blueGem.png'),0.35)))

        ### random gem generation ###
        randEmpty = []
        for i in range(app.maze.row):
            for j in range(app.maze.col):
                if (i > 1 and j > 1 and i < app.maze.row-1 and 
                        j < app.maze.col-1 and app.maze.maze[i][j] != 1):
                    if self.element == 'fire':
                        if manhattanDistance(1,1,i,j) > 8:
                             # ensures gems don't generate too close to the respwan points
                            randEmpty.append((i,j))
                    elif self.element == 'water':
                        if manhattanDistance(1,app.maze.col-1,i,j) > 8:
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
                            # ensures doors don't generate too close to the respwan points
                            randDoor.append((i,j))
                    elif self.element == 'water':
                        if manhattanDistance(1,app.maze.col-1,i,j) > 14:
                            randDoor.append((i,j))
        dx,dy = random.choice(randDoor)
        while isNotValid(app,dx,dy):
            dx,dy = random.choice(randDoor) # make sure the door can be reached
        self.doorPosition.append((dx,dy))
        app.maze.maze[dx][dy] = 9 # represent door

    # checks key presses in maze
    def mazeCharKeyPressed(self,app,event): # put under keyPressed
        if app.AImode == False:
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
    
    # function that checks if gems have been eat
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
    
    # counts hint time, each hint lasts for around 3 seconds
    def hintCounter(self,app):
        if self.hintOn:
            self.hintCount += 1
            if self.hintCount > 30:
                self.hintCount = 0
                self.hintOn =False
                self.hint -= 1

    # places the character each time movement made
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

    # function that finds next target to find path
    def findTarget(self,app):
        if self.doorOpen == False:
            return findShortestMD(self.px,self.py,self.gemPosition)
        else:
            dx,dy = self.doorPosition[0]
            if dx ==0:
                dx = 1
            elif dx == app.maze.row-1:
                dx = app.maze.row-2
            elif dy == 0:
                dy = 1
            elif dy == app.maze.col-1:
                dy = app.maze.col-2
            return dx,dy

    # find the path for hint
    def solvePath(self,app):
        startRow = self.px
        startCol = self.py
        endRow,endCol = self.findTarget(app)
        result = solveMaze(app,startRow,startCol,endRow,endCol)
        if result != None:
            self.path = result
            if self.doorOpen:
                result.extend(self.doorPosition)


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

def aiController(app):
    if app.AImode:
        app.mazeFire.solvePath(app)
        if len(app.mazeFire.path) > 1:
            nextX,nextY = app.mazeFire.path.pop(1)
            app.mazeFire.px = nextX
            app.mazeFire.py = nextY
            
        
# function that creates new character instances
def createNewChar(app):
    app.mazeFire = Char(1,1,'fire')
    app.mazeWater = Char(1,app.maze.col-2,'water')
    
# wrapper put under appStarted in Main
def mazeAppStarted(app):
    app.mazeLevel = 'medium'
    startGame(app)
    
# helper function to make things clearer
def startGame(app):
    createNewMaze(app) # we have a new maze instance
    createNewChar(app) # create mazeFire and mazeWater two maze char instances
    if app.mazeLevel == 'medium':
        app.tileImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('tile1.png'),0.3))
    elif app.mazeLevel == 'easy':
        app.tileImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('tile1.png'),0.4))
    elif app.mazeLevel == 'hard':
        app.tileImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('tile1.png'),0.25))
    app.mazeFire.mazeAppRun(app)
    app.mazeWater.mazeAppRun(app) # load image to characters
    app.AImode = False
    app.AIlevel = 2

# function that put under keyPressed
def mazeKeyPressed(app,event):
    app.mazeFire.mazeCharKeyPressed(app,event)
    app.mazeWater.mazeCharKeyPressed(app,event)
    if event.key == 'r':
        startGame(app)
    elif event.key == 'm':
        if app.mazeLevel == 'easy':
            app.mazeLevel = 'medium'
        elif app.mazeLevel == 'medium':
            app.mazeLevel = 'hard'
        startGame(app)
    elif event.key == 'n':
        if app.mazeLevel == 'hard':
            app.mazeLevel = 'medium'
        elif app.mazeLevel == 'medium':
            app.mazeLevel = 'easy'
        startGame(app)
    if event.key == 'p':
        app.AImode = not app.AImode
    if event.key == '2':
        app.AIlevel = 1
    if event.key == '3':
        app.AIlevel = 2
    if event.key =='4':
        app.AIlevel = 3

# funciton that put under TimeFired in main
def mazeTimerFired(app):
    app.mazeWater.hintCounter(app)
    app.mazeWater.placeChar(app)
    app.mazeFire.placeChar(app)
    # app.mazeWater.findTarget(app)
    app.mazeWater.solvePath(app)
    app.mazeFire.eatGem()
    app.mazeWater.eatGem()
    if app.AImode and app.mazeFire.win == False:
        if app.AIlevel == 1:
            m = 5
        if app.AIlevel == 2:
            m = 3
        elif app.AIlevel == 3:
            m = 1
        if app.counter % m == 0:
            aiController(app)
    else:
        app.mazeFire.hintCounter(app)
        # app.mazeFire.findTarget(app)
        app.mazeFire.solvePath(app)
    
# function that put under redrawAll in main
def mazeRedrawAll(app,canvas):
    drawMaze(app,canvas)


    





