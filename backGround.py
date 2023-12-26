from cmu_112_graphics import *
import character as ca
# spritesheets and graphs from: 
# https://github.com/RRCAT920/Fireboy-and-Watergirl/tree/master/assets

# there will be three kinds of map components:
# floors, ceilings, and walls
# -if ceilings are touched, veritcal velocity changes to negative and 
# drops by gravity
# -if floors are touched, vertical velocity becomes zero
# -if walls are touched, x-coordinate remains unchanged(character pushed back)

class Floor(object):
    def __init__(self):
        self.floors = [] # a list containing all floor positions
                         # stored as a tuple with four coordinates
        self.floatingFloors = [] 
            # a list containing horizontally movable floors
        # self.floatingFloorFlag = False #floor has not been activated yet
        self.lift = []
        self.gate = []
        # self.liftdown = [(40,350,150,350)]
        self.liftAdder = 2 # lift movement speed
        self.buttons = []
        self.floorMoveCounter = 0
        self.floorMoveX = 0
        self.floorMoveY = 0
        self.liftFlag = False # changed by button press
        self.addflag = False # flag used in moving floating board
        self.adder = 10

    def runAppLevel1(self,app):
        self.floors = createLevel1Floor(app)
        self.buttons = createLevel1Button()
        self.floatingFloors = [(200,450,280,450)]
        self.lift = [(40,400,150,400)]
        app.level1Floors = self # defines floor object in Main
    
    def runAppLevel2(self,app):
        self.floors = createLevel2Floor(app)
        self.buttons = createLevel2Button()
        self.floatingFloors = [(570,450,650,450)]
        self.lift = [(300,200,400,200)]
        self.gate = [(650,0,650,150)]
        app.level2Floors = self # defines floor object in Main
        

    def checkOnFloor(self,app):
        # function that checks if any of the characters are on the ground
        fx,fy = app.fireBoy.px, app.fireBoy.py
        wx,wy = app.waterGirl.px, app.waterGirl.py
        fireflag = False
        waterflag = False
        # flag if to decide whether the character is on any of the floors
        firefloorY = 0
        waterfloorY = 0
        for (x0,y0,x1,y1) in self.floors:
            if (fx>x0-20 and fx<x1+20) and (y0-70 < fy < y0): 
                # hard-coded, need change later
                app.fireBoy.inair = False
                # if on the ground, stop moving vertically
                fireflag = True
                firefloorY = y0-60 # hard-coded
            if (wx>x0-20 and wx<x1+20) and (y0-60 < wy < y0+10):
                # hard-coded, need change later
                app.waterGirl.inair = False
                waterfloorY = y0-55 # hard-coded
                waterflag = True
        if fireflag == False:
            app.fireBoy.inair = True
        else:
            app.fireBoy.py = firefloorY
        if waterflag == False:
            app.waterGirl.inair = True # if not on the ground, in the air
        else:
            app.waterGirl.py = waterfloorY # if on the ground, 
                                           # place the character
    
    def floorTimer1(self):
        for i in range(len(self.floors)):
            if self.floors[i] in self.floatingFloors:
                (x0,y0,x1,y1) = self.floors[i]
                if self.addflag == True:
                    self.adder = 10
                    if x0 < 400:
                        x0 += self.adder
                        x1 += self.adder
                    else:
                        self.addflag = False
                elif self.addflag == False:
                    self.adder = -10
                    if x0 > 200:
                        x0 += self.adder
                        x1 += self.adder
                    else:
                        self.addflag = True
                self.floors[i] = (x0,y0,x1,y1)
                self.floatingFloors = [(x0,y0,x1,y1)]
    
    def floorTimer2(self):
        for i in range(len(self.floors)):
            if self.floors[i] in self.floatingFloors:
                (x0,y0,x1,y1) = self.floors[i]
                if self.addflag == True:
                    self.adder = 10
                    if x0 < 750:
                        x0 += self.adder
                        x1 += self.adder
                    else:
                        self.addflag = False
                elif self.addflag == False:
                    self.adder = -10
                    if x0 > 570:
                        x0 += self.adder
                        x1 += self.adder
                    else:
                        self.addflag = True
                self.floors[i] = (x0,y0,x1,y1)
                self.floatingFloors = [(x0,y0,x1,y1)]

        
    
    def checkLevel1Button(self): # elevator respond to button press
        for i in range(len(self.floors)):
            if self.floors[i] in self.lift:
                (x0,y0,x1,y1) = self.floors[i]
                if self.liftFlag == False:
                    self.liftAdder = 2
                    if y0 < 400:
                        y0 += self.liftAdder
                        y1 += self.liftAdder
                elif self.liftFlag == True:
                    self.liftAdder = -2
                    if y0 > 250:
                        y0 += self.liftAdder
                        y1 += self.liftAdder
                self.floors[i] = (x0,y0,x1,y1)
                self.lift = [(x0,y0,x1,y1)]

    def checkLevel2Button(self):
        for i in range(len(self.floors)):
            if self.floors[i] in self.lift:
                (x0,y0,x1,y1) = self.floors[i]
                if self.liftFlag == True:
                    self.liftAdder = 2
                    if y0 < 400:
                        y0 += self.liftAdder
                        y1 += self.liftAdder
                elif self.liftFlag == False:
                    self.liftAdder = -2
                    if y0 > 200:
                        y0 += self.liftAdder
                        y1 += self.liftAdder
                self.floors[i] = (x0,y0,x1,y1)
                self.lift = [(x0,y0,x1,y1)]

    def drawFloor(self,app,canvas):
        for (x0,y0,x1,y1) in self.floors:
            canvas.create_line(x0,y0,x1,y1,fill = 'white',width = 4)

class Ceiling(object):
    def __init__(self):
        self.ceilings = [] # ceilings stored as four-element tuples

    def runAppLevel1(self,app):
        self.ceilings = createLevel1Ceilings(app) 
        app.level1Ceilings = self # defines ceiling object in appStarted
    
    def runAppLevel2(self,app):  
        self.ceilings = createLevel2Ceilings(app)
        app.level2Ceilings = self
    
    def checkHitCeiling(self,app):
        # checks if characters hit ceilings
        fx,fy = app.fireBoy.px, app.fireBoy.py
        wx,wy = app.waterGirl.px, app.waterGirl.py
        for (x0,y0,x1,y1) in self.ceilings:
            if (fx>x0-20 and fx<x1+20) and (0<fy-y0<30): 
                # app.fireBoy.dy = -app.fireBoy.dy
                app.fireBoy.dy = 20 
            if (wx>x0-20 and wx<x1+20) and (-10<wy-y0<40):
                app.waterGirl.dy = 20 # change of direction


    def drawCeiling(self,app,canvas):
        for (x0,y0,x1,y1) in self.ceilings:
            canvas.create_line(x0,y0,x1,y1,fill = 'white',width = 4)

class Wall(object):
    def __init__(self):
        self.walls = []
        self.liftWall = [(650,0,650,150)]
        self.wallLiftAdder = 2
        self.wallFlag = False
    
    def runAppLevel1(self,app):
        self.walls = createLevel1Walls(app)
        app.level1Walls = self
    
    def runAppLevel2(self,app):
        self.walls = createLevel2Walls(app)
        app.level2Walls = self

    # helper function that checks if the character hits the wall
    def checkHitWalls(self,app):
        fx,fy = app.fireBoy.px, app.fireBoy.py
        wx,wy = app.waterGirl.px, app.waterGirl.py
        for (x0,y0,x1,y1) in self.walls:
            if 0 < x0-fx < 50:
                if y0-30 < fy < y1+30 and app.fireBoy.dx > 0:
                    app.fireBoy.dx = 0
                    app.fireBoy.px = x0 - 25
            elif 0 < fx-x0 < 50:
                if y0-30 < fy < y1+30 and app.fireBoy.dx < 0:
                    app.fireBoy.dx = 0
                    app.fireBoy.px = x0 + 25
            if 0 < x0-wx < 70:
                if y0-30 < wy < y1+30 and app.waterGirl.dx > 0:
                    app.waterGirl.dx = 0
                    app.waterGirl.px = x0 - 30
            elif 0 < wx-x0 < 70:
                if y0-30 < wy < y1+30 and app.waterGirl.dx < 0:
                    app.waterGirl.dx = 0  
                    app.waterGirl.px = x0 + 30 

    def checkLevel2Wall(self):
        for i in range(len(self.walls)):
            if self.walls[i] in self.liftWall:
                (x0,y0,x1,y1) = self.walls[i]
                if self.wallFlag == False:
                    self.liftAdder = 2
                    if y1 < 150:
                        y0 += self.liftAdder
                        y1 += self.liftAdder
                elif self.wallFlag == True:
                    self.liftAdder = -2
                    if y1 > 0:
                        y0 += self.liftAdder
                        y1 += self.liftAdder
                self.walls[i] = (x0,y0,x1,y1)
                self.liftWall = [(x0,y0,x1,y1)]
        

    def drawWalls(self,app,canvas):
        for (x0,y0,x1,y1) in self.walls:
            canvas.create_line(x0,y0,x1,y1,fill = 'white',width = 4) 

class Button(object):
    # buttons are semi-circles with colors representing characters 
    def __init__(self,position,color):
        self.position = position
        self.color = color
        self.pressed = False
        self.buttons = []

    def drawButton(self,canvas):
        if self.pressed == False:
            x0,y0,x1,y1 = self.position
            canvas.create_arc(x0,y0,x1,y1,fill=f'{self.color}',start = 0,extent = 180)



def createLevel1Button():
    # create two buttons instances
    redButton= Button((510,500,550,520),'red')
    blueButton = Button((250,240,290,260),'blue')
    # wrapper that put two instances into a list
    button = []
    button.append(redButton)
    button.append(blueButton)
    return button

def createLevel2Button():
    # create two buttons instances
    redButton1 = Button((480,410,520,390),'red')
    redButton2 = Button((700,160,740,140),'cyan')
    blueButton = Button((70,340,110,320),'blue')
    # wrapper that put two instances into a list
    button = []
    button.append(redButton1)
    button.append(redButton2)
    button.append(blueButton)
    return button

# helper function put under timerFired in Main to check if button pressed
def checkPressedTimer(app):
    fx, fy = app.fireBoy.px, app.fireBoy.py
    wx, wy = app.waterGirl.px,app.waterGirl.py
    fPressed = False
    wPressed = False
    if app.gameLevel == 'Level 1':
        b = app.level1Floors.buttons
    else:
        b = app.level2Floors.buttons
    for button in b:
        x0,y0,x1,y1 = button.position
        cx, cy = (x1-x0)/2, (y1+y0)/2
        if button.color == 'red':
            if x0< fx< x1 and  (0<cy-fy<80):
                button.pressed = True
                fPressed = True
            else:
                button.pressed = False
                fPressed = False
        elif button.color == 'blue':
            if x0 < wx < x1 and (0< cy-wy< 80):
                button.pressed = True
                wPressed = True
            else:
                button.pressed = False
                wPressed = False
        elif button.color == 'cyan':
            if x0< fx< x1 and  (0<cy-fy<80):
                button.pressed = True
                cPressed = True
            else:
                button.pressed = False
                cPressed = False
    if app.gameLevel == 'Level 1':
        app.level1Floors.liftFlag = wPressed or fPressed
    else:
        app.level2Floors.liftFlag = wPressed or fPressed or cPressed
        app.level2Walls.wallFlag = wPressed or fPressed or cPressed

def createLevel1Floor(app):
    # map with all the floors
    floor = []
    # floor 1
    floor.append((40,700,400,700)) # linear floors
    floor.append((550,700,700,700))
    floor.append((850,700,1170,700))
    floor.append((40,580,200,580))
    # pool 1
    floor.append((420,720,530,720))
    floor.append((400,700,420,720))
    floor.append((530,720,550,700))
    # pool 2
    floor.append((700,700,720,720))
    floor.append((720,720,830,720))
    floor.append((830,720,850,700))
    # stair floor 1
    floor.append((1070,630,1170,630))
    # floor 2
    floor.append((900,550,950,550))
    floor.append((800,510,900,510))
    # pool 3
    floor.append((670,530,780,530))
    floor.append((650,510,670,530))
    floor.append((780,530,800,510))
    # floor 2 with stairs:
    floor.append((500,510,650,510))
    # floating floor:
    floor.append((200,450,280,450)) # floating floor
    # Lift floor 2: left end
    floor.append((40,400,150,400)) # Lift floor(with button)
    # floor 3 1
    floor.append((200,250,430,250))
    # floor 3 2
    floor.append((550,250,600,250))
    # floor 3 pool 1
    floor.append((430,250,450,270))
    floor.append((530,270,550,250))
    floor.append((450,270,530,270))
    # floor 3 3
    floor.append((600,250,1100,250))
    # floor 4 
    floor.append((1000,190,1100,190))
    # floor 5
    floor.append((750,120,950,120))
    return floor

def createLevel2Floor(app):
    floor = []
    floor.append((40,580,200,580)) # respawn platform
    # floor 1 1
    floor.append((40,700,250,700)) 
    # floor 1 2
    floor.append((250,680,300,680))
    # floor 1 pool 1
    floor.append((300,680,320,700))
    floor.append((320,700,380,700))
    floor.append((380,700,400,680))
    # floor 1 3
    floor.append((400,680,450,680))
    # floor 1 pool 2
    floor.append((450,680,470,700))
    floor.append((470,700,530,700))
    floor.append((530,700,550,680))
    # floor 1 4
    floor.append((550,680,600,680))
    # floor 1 pool 3
    floor.append((600,680,620,700))
    floor.append((620,700,680,700))
    floor.append((680,700,700,680))
    # floor 1 5
    floor.append((700,680,750,680))
    # floor 1 pool 4:
    floor.append((750,680,770,700))
    floor.append((770,700,830,700))
    floor.append((830,700,850,680))
    # floor 1 6
    floor.append((850,680,900,680))
    # floor 0:
    floor.append((900,750,1170,750))
    # floor 1.5
    floor.append((1000,600,1170,600))
    # floor 2 1
    floor.append((850,510,950,510))
    #### floating board ########
    floor.append((570,450,650,450))
    ############################
    # floor 2 2
    floor.append((450,400,550,400))
    # floor 2 pool 5
    floor.append((430,420,450,400))
    floor.append((270,420,430,420))
    floor.append((250,400,270,420))
    # floor 2 3
    floor.append((200,400,250,400))
    # floor 2.5 
    floor.append((40,330,150,330))
    ### elevator ###############
    floor.append((300,200,400,200))
    ############################
    floor.append((500,150,1170,150))
    floor.append((925,95,1000,95))
    return floor

def createLevel1Ceilings(app):
    # map with all the ceilings
    ceilings = []
    ceilings.append((40,595,200,595))
    # floor 2 ceiling 1
    ceilings.append((880,570,950,570))
    # floor 2 ceiling 2
    ceilings.append((500,540,880,540))
    # floor 2 ceiling 3
    ceilings.append((40,430,150,430))
    # floor 3 ceiling 1
    ceilings.append((200,280,1100,280))
    # floor 4 ceiling
    ceilings.append((1000,200,1100,200))
    # floor 5 ceiling 1
    ceilings.append((750,130,950,130))
    return ceilings

def createLevel2Ceilings(app):
    ceilings = []
    ceilings.append((40,595,200,595))
    # ceiling 1.5
    ceilings.append((1000,620,1170,620))
    # ceiling 2.5
    ceilings.append((40,350,150,350))
    # floor 2 ceiling 
    ceilings.append((200,430,550,430))
    # floor 3 ceiling
    ceilings.append((500,170,1170,170))
    # floor 4 ceiling
    ceilings.append((925,105,1000,105))
    return ceilings

def createLevel1Walls(app):
    walls = []
    walls.append((40,50,40,750))
    walls.append((1170,50,1170,750))
    walls.append((200,580,200,595))
    # floor 1 wall 1
    walls.append((1070,630,1070,700))
    # floor 2 wall 1
    walls.append((950,550,950,570))
    # floor 2 wall 2
    walls.append((900,510,900,550))
    # floor 2 wall 3
    walls.append((880,540,880,570))
    # floor 2 wall 4
    walls.append((500,510,500,540))
    # floor 2 wall 5
    walls.append((150,430,150,400))
    # floor 3 wall 1
    walls.append((200,250,200,280))
    # floor 5 wall 1
    walls.append((750,120,750,130))
    # floor 5 wall 2
    walls.append((950,120,950,130))

    walls.append((1100,190,1100,280))
    return walls

def createLevel2Walls(app):
    walls = []
    walls.append((200,580,200,595))
    walls.append((250,680,250,700))
    walls.append((900,680,900,750))
    # wall 1.5
    walls.append((1000,600,1000,620))
    # floor 2 wall 1 & 2
    walls.append((550,430,550,400))
    walls.append((200,400,200,430))
    # floor 2.5 wall 
    walls.append((150,330,150,350))
    # floor 3 wall 3
    walls.append((500,150,500,170))

    ### floating wall#############
    walls.append((650,0,650,150))
    ##############################
    walls.append((1000,95,1000,150))
    # edge
    walls.append((1170,0,1170,750))
    walls.append((40,0,40,750))
    return walls

#####################################################
mapLevel1Floor = Floor()
mapLevel1Ceilings = Ceiling()
mapLevel1Walls = Wall()
# three Level 1 instance created for the Main to use
mapLevel2Floor = Floor()
mapLevel2Ceilings = Ceiling()
mapLevel2Walls = Wall()
#####################################################


def getIcon(): # helper function that sets all icons
    icon = []
    icon += [(600,400),(600,500),(600,600),(100,100),(600,400),(600,500),(100,100)
             ,(100,100),(100,100),(100,100)]  
    return icon

def getIconPress(): # bools used to check if any icons are clicked
    icon = [False for i in range(10)]
    return icon

def getIconText(): # helper function that sets all icon text
    text = []
    text.append('Normal Mode') # icon 1 splash screen No.0
    text.append('Maze Mode') # icon 2 splash screen No.1
    text.append('Help Menu') # icon 3 splash screen No.2
    text.append('Back') # icon on help screen No.3
    text.append('Level 1') # icon 1 on normal mode sub No.4
    text.append('Level 2') # icon 2 on normal mode sub No.5
    text.append('Back') # icon on normal mode level sub No.6
    text.append('Back') # icon on normal mode level 2 No.7
    text.append('Back') # icon on Maze mode No.8
    text.append('Back') # icon on normal mode level 1 No.9
    return text

def getIconColors(): # helper function that sets all icon colors
    color = ['aqua' for i in range(10)]
    return color

######################################
## splashScreenMode helper functions
######################################
def createSplashScreenIcons(app):
    app.icons = getIcon()
    # app.iconsOn = getIconStatus()
    app.iconsPressed = getIconPress()
    app.iconsColor = getIconColors()
    app.iconsText = getIconText()

def splashTimer(app): # detects icon presses
    for i in range(7):
        if app.iconsPressed[i] == True:
            if i == 0:
                app.iconsPressed[i] = False # resets icon status
                app.levelScreen = True
            if i == 1:
                app.iconsPressed[i] = False
                app.mode = 'gameMode'
                app.gameLevel = 'Maze'
            if i == 2:
                app.iconsPressed[i] = False
                app.mode = 'helpMode'
            if i == 4:
                app.iconsPressed[i] = False
                app.mode = 'gameMode'
                app.gameLevel = 'Level 1'
            if i == 5:
                app.iconsPressed[i] = False
                app.mode = 'gameMode'
                app.gameLevel = 'Level 2'
            if i == 6:
                app.iconsPressed[i] = False
                app.levelScreen = False
    app.waterGirl.timeRuns()
    app.fireBoy.timeRuns() # make the drawing of the character 
                           # on the splash screen dynamic

def splashMouseMoved(app,event):
    cx,cy = event.x,event.y
    if app.levelScreen == False:
        for i in range(3):
            ix,iy = app.icons[i]
            xRange = (len(app.iconsText[i])) * 25 /2
            if cy-30 < iy < cy+30 and cx-xRange < ix < cx+xRange:
                app.iconsColor[i] = 'red'
            else:
                app.iconsColor[i] = 'aqua'
    else:
        for i in range(3,7):
            ix,iy = app.icons[i]
            xRange = (len(app.iconsText[i])) * 25 /2
            if cy-30 < iy < cy+30 and cx-xRange < ix < cx+xRange:
                app.iconsColor[i] = 'red'
            else:
                app.iconsColor[i] = 'aqua'

def splashMousePressed(app,event):
    cx,cy = event.x,event.y
    if app.levelScreen == False:
        for i in range(3):
            ix,iy = app.icons[i]
            xRange = (len(app.iconsText[i])) * 25 /2
            if cy-30 < iy < cy+30 and cx-xRange < ix < cx+xRange:
                app.iconsPressed[i] = True
    else:
        for i in range(3,7):
            ix,iy = app.icons[i]
            xRange = (len(app.iconsText[i])) * 25 /2
            if cy-30 < iy < cy+30 and cx-xRange < ix < cx+xRange:
                app.iconsPressed[i] = True
    
def gameModeMousePressed(app,event):
    cx,cy = event.x,event.y
    if app.gameLevel == 'Level 2':
        ix,iy = app.icons[7]
        xRange = (len(app.iconsText[7])) * 25 /2
        if cy-30 < iy < cy+30 and cx-xRange < ix < cx+xRange:
            app.iconsPressed[7] = True
    elif app.gameLevel == 'Maze':
        ix,iy = app.icons[8]
        xRange = (len(app.iconsText[8])) * 25 /2
        if cy-30 < iy < cy+30 and cx-xRange < ix < cx+xRange:
            app.iconsPressed[8] = True
    elif app.gameLevel == 'Level 1':
        ix,iy = app.icons[9]
        xRange = (len(app.iconsText[9])) * 25 /2
        if cy-30 < iy < cy+30 and cx-xRange < ix < cx+xRange:
            app.iconsPressed[9] = True

def gameModeMouseMoved(app,event):
    cx,cy = event.x,event.y
    for i in range(7,10):
        ix,iy = app.icons[i]
        xRange = (len(app.iconsText[i])) * 25 /2
        if cy-30 < iy < cy+30 and cx-xRange < ix < cx+xRange:
            app.iconsColor[i] = 'red'
        else:
            app.iconsColor[i] = 'aqua'



def drawIconsInGameMode(app,canvas):
    font = 'Algerian 35 bold'
    if app.gameLevel == 'Level 2':
        x,y = app.icons[7]
        canvas.create_text(x,y,text = app.iconsText[7],fill = app.iconsColor[7],font = font)
    elif app.gameLevel == 'Maze':
        x,y = app.icons[8]
        canvas.create_text(x,y,text = app.iconsText[8],fill = app.iconsColor[8],font = font)
    elif app.gameLevel == 'Level 1':
        x,y = app.icons[9]
        canvas.create_text(x,y,text = app.iconsText[9],fill = app.iconsColor[9],font = font)

def drawIconsInSplash(app,canvas): # three icons used in splashScreen
    font = 'Algerian 35 bold'
    if app.levelScreen == False:
        for i in range(3):
            x,y = app.icons[i]
            canvas.create_text(x,y,text = app.iconsText[i],fill = app.iconsColor[i],font = font)
    else:
        for i in range(3,7):
            x,y = app.icons[i]
            canvas.create_text(x,y,text = app.iconsText[i],fill = app.iconsColor[i],font = font)
    

def drawImage(app,canvas):
    canvas.create_image(600,150,image = ImageTk.PhotoImage(app.title))

def drawCharacter(app,canvas):
    # drawing of little fireBoy on the left of splashscreen
    fbodySprite = app.fireBoy.image.fireBodySheets[app.fireBoy.bodyIndex]
    fbodyImg = fbodySprite[app.fireBoy.bodySpriteCount[app.fireBoy.bodyIndex]]
    fheadSprite = app.fireBoy.image.fireHeadSheets[app.fireBoy.headIndex]
             # this index will change in the future as more moves added
    fheadImg = fheadSprite[app.fireBoy.headSpriteCount[app.fireBoy.headIndex]]
    canvas.create_image(300-13,500+40, image=ImageTk.PhotoImage(fbodyImg))
    canvas.create_image(300,500, image=ImageTk.PhotoImage(fheadImg))
    # drawing of little waterGirl on the right of splashscreen
    wbodySprite = app.waterGirl.image.waterBodySheets[app.waterGirl.bodyIndex]
    wbodyImg = wbodySprite[app.waterGirl.bodySpriteCount[app.waterGirl.bodyIndex]]
    wheadSprite = app.waterGirl.image.waterHeadSheets[app.waterGirl.headIndex]
    wheadImg = wheadSprite[app.waterGirl.headSpriteCount[app.waterGirl.headIndex]]
    canvas.create_image(900-1,500+32, image=ImageTk.PhotoImage(wbodyImg))
    canvas.create_image(900,500, image=ImageTk.PhotoImage(wheadImg))
##############################################################################

############################################
## help mode helper functions
############################################
def drawIconInHelp(app,canvas):
    font = 'Algerian 35 bold'
    x,y = app.icons[3]
    canvas.create_text(x,y,text = app.iconsText[3],fill = app.iconsColor[3],font = font)

def drawTextInHelp(app,canvas):
    font = 'Arial 20 bold'
    canvas.create_image(600,400,image=app.splashBackGround)
    canvas.create_text(600,200,
        text = '{:<30}'.format('Click Normal Mode for the classic FireBoy and WaterGirl Game!'),
        fill = 'white',font=font)
    canvas.create_text(600,250,
        text = '{:<30}'.format('in this mode, two players need to work together to get to the end'),
        fill = 'white',font=font)
    canvas.create_text(600,300,
        text =  '{:<30}'.format('use "wasd" to control waterGirl and "arrows" to control fireBoy\n'),
        fill='white',font=font)
    canvas.create_text(600,350,
        text = '{:<30}'.format('Remember that FireBoy is afraid of water and WaterGirl fears fire along the way'),
        fill = 'white',font = font)
    canvas.create_text(600,450,text= '{:<60}'.format('Click Maze Mode for a special designed mode to play'),
        fill='white',font=font)
    canvas.create_text(600,500,text= '{:<15}'.format('in this mode two players are competing against each other in a maze'),
        fill='white',font=font)
    canvas.create_text(600,550,text= '{:<30}'.format('first you need to collect all the gems to open your exit'),
        fill='white',font=font)
    canvas.create_text(600,600,text= '{:<30}'.format('yet you can press "h" or "1" to reveal a hint'),
        fill='white',font=font)
    canvas.create_text(600,640,text= '{:<30}'.format('in the end the first one out wins the game'),
            fill='white',font=font)

def helpMouseMoved(app,event): # helper function detects mouse move in helpMode
    cx,cy = event.x,event.y
    ix,iy = app.icons[3]
    xRange = (len(app.iconsText[3])) * 25 /2
    if cy-30 < iy < cy+30 and cx-xRange < ix < cx+xRange:
        app.iconsColor[3] = 'red'
    else:
        app.iconsColor[3] = 'aqua'

# helper function detects mouse press in helpMode
def helpMousePressed(app,event):
    cx,cy = event.x,event.y
    ix,iy = app.icons[3]
    xRange = (len(app.iconsText[3])) * 25 /2
    if cy-30 < iy < cy+30 and cx-xRange < ix < cx+xRange:
        app.iconsPressed[3] = True








        




            
            


    
    

