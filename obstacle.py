from cmu_112_graphics import *
import math

class Bullet(object): # class of bullets shot by the cannon
    def __init__(self,color,position,direction):
        self.color = color
        self.position = position
        self.direction = direction
        self.counter = 0
    
    # checks if the bullet hits the character
    def checkHit(self,app):
        fx,fy = app.fireBoy.px,app.fireBoy.py
        wx,wy = app.waterGirl.px,app.waterGirl.py
        x, y = self.position
        if math.sqrt((fx-x)**2+(fy-y)**2)< 46 and self.color == 'blue':
            return True
        elif math.sqrt((wx-x)**2+(wy-y)**2)< 46 and self.color == 'red':
            return True
        return False


def bulletAppStarted(app): # function put under appStarted in Main
    app.bullet = []

def generateBullet(app): # function that generates bullets in Main, put under timerFired
    if app.counter % 30 == 0:
        if app.counter % 60  == 0:
            if app.gameLevel == 'Level 1':
                fx, fy = app.fireBoy.px, app.fireBoy.py+60
                x,y = (fx-1050,fy-250)
                dx = x/math.sqrt(x**2+y**2)
                dy = y/math.sqrt(x**2+y**2) # unit direction vector
                newB = Bullet('blue',(1050,230),(dx,dy))
                app.bullet.append(newB)
            elif app.gameLevel == 'Level 2':
                fx, fy = app.fireBoy.px, app.fireBoy.py+60
                x,y = (fx-1050,fy-150)
                dx = x/math.sqrt(x**2+y**2)
                dy = y/math.sqrt(x**2+y**2) # unit direction vector
                newB = Bullet('blue',(950,135),(dx,dy))
                app.bullet.append(newB)
        else:
            if app.gameLevel == 'Level 1':
                wx, wy = app.waterGirl.px, app.waterGirl.py+64
                x,y = (wx-1050,wy-250)
                dx = x/math.sqrt(x**2+y**2)
                dy = y/math.sqrt(x**2+y**2) # unit direction vector
                newB = Bullet('red',(1050,230),(dx,dy))
                app.bullet.append(newB)
            elif app.gameLevel == 'Level 2':
                wx, wy = app.waterGirl.px, app.waterGirl.py+64
                x,y = (wx-1050,wy-150)
                dx = x/math.sqrt(x**2+y**2)
                dy = y/math.sqrt(x**2+y**2) # unit direction vector
                newB = Bullet('red',(950,135),(dx,dy))
                app.bullet.append(newB)
    i = 0
    while i < len(app.bullet):  # move bullets
        if app.bullet[i].checkHit(app) and app.testing == False:
            app.gameOver = True
        px,py = app.bullet[i].position
        dx,dy = app.bullet[i].direction
        px += dx*15
        py += dy*15
        if px < 0 or px > app.width or py < 0 or py > app.height:
            app.bullet.pop(i)
        elif checkCollision(app,px,py) == True:
            app.bullet.pop(i)
        else:
            app.bullet[i].position = (px,py)
            i += 1

# functino that checks if the bullet collides with background, put under timerFired
def checkCollision(app,px,py):
    if app.gameLevel == 'Level 1':
        for wall in app.level1Walls.walls:
            x0,y0,x1,y1 = wall
            if y0 < py < y1 and 0<px-x0 < 10:
                return True
        for floor in app.level1Floors.floors:
            x0,y0,x1,y1 = floor
            if x0 < px < x1 and 0<y0-py < 10:
                return True
        for ceiling in app.level1Ceilings.ceilings:
            x0,y0,x1,y1 = ceiling
            if x0 < px < x1 and 0< py-y0 < 10:
                return True
    elif app.gameLevel == 'Level 2':
        for wall in app.level2Walls.walls:
            x0,y0,x1,y1 = wall
            if y0 < py < y1 and -15< px-x0 < 15:
                return True
        for floor in app.level2Floors.floors:
            x0,y0,x1,y1 = floor
            if x0 < px < x1 and 0< y0-py < 10:
                return True
        for ceiling in app.level2Ceilings.ceilings:
            x0,y0,x1,y1 = ceiling
            if x0 < px < x1 and 0< py-y0 < 10:
                return True
    
def drawBullet(app,canvas):
    for bullet in app.bullet:
        cx,cy = bullet.position
        canvas.create_oval(cx-10,cy-10,cx+10,cy+10,fill = bullet.color)

class Door(object): # class that contains the final doors (destination)
    def __init__(self,position,color):
        self.color = color
        self.position = position
        self.open = False
    
    def checkInDoor(self,app): 
        fx,fy = app.fireBoy.px,app.fireBoy.py
        wx,wy = app.waterGirl.px,app.waterGirl.py
        x,y = self.position
        if self.color == 'red':
            if x-50 < fx < x+50 and abs(fy-y) < 70:
                self.open = True
            else:
                self.open = False
        elif self.color == 'blue':
            if x-50 < wx < x+50 and abs(wy-y) < 70:
                self.open = True
            else:
                self.open = False
    
def doorAppStartedLevel1(app):
    app.level1doors = [Door((800,75),'red'),Door((900,75),'blue')]

def doorAppStartedLevel2(app):
    app.level2doors = [Door((1050,110),'red'),Door((1150,110),'blue')]

 
def checkGameClear(app): # checks if in door
    if app.gameLevel == 'Level 1':
        d = app.level1doors
    elif app.gameLevel == 'Level 2':
        d = app.level2doors  #### add door later
    for door in d:
        door.checkInDoor(app)
        if door.open == False:
            return False
    app.fireBoy.headIndex = 0
    app.fireBoy.bodyIndex = 0
    app.waterGirl.headIndex = 0
    app.waterGirl.bodyIndex = 0
    app.gameClear = True
    return True

def drawDoors(app,canvas):
    if app.gameLevel == 'Level 1':
        d = app.level1doors
    elif app.gameLevel == 'Level 2':
        d = app.level2doors  #### add door later
    for door in d:
        x,y=door.position
        if door.color == 'red':
            canvas.create_image(x,y,image=ImageTk.PhotoImage(app.fireDoor))
        else:
            canvas.create_image(x,y,image = ImageTk.PhotoImage(app.waterDoor))

class Pool(object):
    def __init__(self,position,color):
        self.position = position # polygon with four pairs of coordinates
        self.color = color
    
    # checks if the character is in the pool
    def checkHit(self,app):
        fx,fy = app.fireBoy.px,app.fireBoy.py
        wx,wy = app.waterGirl.px,app.waterGirl.py
        x0,y0,q,w,e,r,x1,y1 = self.position # we only need x0,y0,x1,y1
        if self.color == 'blue':
            if x0<fx<x1 and 0<(y0-fy)<50 :
                return True
        elif self.color == 'red':
            if x0<wx<x1 and 0<(y0-wy)<50 :
                return True
        elif self.color == 'limegreen':
            if (x0<fx<x1 and -25<(y0-fy)<50) or  (x0<wx<x1 and -25<(y0-wy)<50):
                return True
        return False

def poolAppStartedLevel1(app):
    pool1 = Pool((405,705,420,720,530,720,545,705),'red')
    pool2 = Pool((705,705,720,720,830,720,845,705),'blue')
    pool3 = Pool((655,515,670,530,780,530,795,515),'limegreen')
    pool4 = Pool((435,255,450,270,530,270,545,255),'red')
    poolList = [pool1,pool2,pool3,pool4]
    app.level1pools = poolList

def poolAppStartedLevel2(app): # add later for level 2
    pool1 = Pool((305,685,320,700,380,700,395,685),'blue')
    pool2 = Pool((455,685,470,700,530,700,545,685),'red')
    pool3 = Pool((605,685,620,700,680,700,695,685),'blue')
    pool4 = Pool((755,685,770,700,830,700,845,685),'red')
    pool5 = Pool((900,700,900,750,1170,750,1170,700),'limegreen')
    pool6 = Pool((255,405,270,420,430,420,445,405),'limegreen')
    poolList = [pool1,pool2,pool3,pool4,pool5,pool6]
    app.level2pools = poolList

# checks if player falls into leathal pools
def poolGameOver(app):
    if app.gameLevel == 'Level 1':
        p = app.level1pools
    else:
        p = app.level2pools
    for pool in p:
        if pool.checkHit(app):
            app.gameOver = True
            return True
    return False

def drawPools(app,canvas):
    if app.gameLevel == 'Level 1':
        p = app.level1pools
    else:
        p = app.level2pools
    for pool in p:
        x0,y0,x1,y1,x2,y2,x3,y3 = pool.position
        color = pool.color
        canvas.create_polygon(x0,y0,x1,y1,x2,y2,x3,y3,fill = color)


        


        







        
