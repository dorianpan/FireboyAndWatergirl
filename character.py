import spriteSheets as spS
import math
from cmu_112_graphics import *

# spritesheets and graphs from: 
# https://github.com/RRCAT920/Fireboy-and-Watergirl/tree/master/assets

# class of characters and their attributes, sprite images, and positions.
class Character(object):
    def __init__(self,element,px,py,image):
        self.element = element # either fire or water
        self.px = px
        self.py = py
        self.inair = False
        self.gravity = 9
        self.dx = 0
        self.dy = 0
        self.image = image # a spriteSheet object
        self.counter = 0
        self.bodySpriteCount = [0]
        self.headSpriteCount = [0,0] # lists that keeps track of 
                                   # spritesheet indices
        self.headIndex = 0
        self.bodyIndex = 0 # indices tells which part of animation to draw

    # called under keyPressed in Main
    def move(self,event):
        if self.element == 'fire':
            if event.key == 'Right':
                self.dx = 20
            elif event.key == 'Left':
                self.dx = -20
            if self.inair == False and event.key == 'Up':
                self.inair = True
                self.dy = -30
        if self.element == 'water':
            if event.key == 'd':
                self.dx = 20
            elif event.key == 'a':
                self.dx = -20
            if self.inair == False and event.key == 'w':
                self.inair = True
                self.dy = -30

    # called under keyReleased in Main
    def keyReleased(self,event):
        if self.element == 'fire':
            if event.key == 'Right' or event.key == 'Left':
                self.dx = 0
        if self.element == 'water':
            if event.key == 'd' or event.key == 'a':
                self.dx = 0
 
    
    # called under timerFired
    def timeRuns(self):
        if self.inair == True:
            self.py += self.dy
            self.dy += self.gravity
        elif self.inair == False:
            self.dy = 0
        self.px += self.dx
        self.headSpriteCount = []
        self.bodySpriteCount = []
        if self.element == 'fire':
            for imgL in self.image.fireHeadSheets:
                self.headSpriteCount.append(self.counter % len(imgL))
            for imgL in self.image.fireBodySheets:
                self.bodySpriteCount.append(self.counter % len(imgL))
        else:
            for imgL in self.image.waterHeadSheets:
                self.headSpriteCount.append(self.counter % len(imgL))
            for imgL in self.image.waterBodySheets:
                self.bodySpriteCount.append(self.counter % len(imgL))
        self.counter += 1
        # need water run sprite!
        if self.dx != 0 and self.headIndex == 0:
            self.headIndex = 1
            self.bodyIndex = 1
        elif self.headIndex == 1 and self.dx == 0:
            self.headIndex = 0
            self.bodyIndex = 0

    # called under redrawAll, draws the character according to its position
    def drawCharacter(self, app, canvas):
        if self.element == 'fire':
            bodySprite = self.image.fireBodySheets[self.bodyIndex]
            bodyImg = bodySprite[self.bodySpriteCount[self.bodyIndex]]
            if self.bodyIndex == 0:
                canvas.create_image(self.px-13,self.py+40, image=ImageTk.PhotoImage(bodyImg))
            elif self.bodyIndex == 1:
                if self.dx < 0:
                    bodyImg = bodyImg.transpose(Image.FLIP_LEFT_RIGHT)
                    canvas.create_image(self.px,self.py+40,image=ImageTk.PhotoImage(bodyImg))
                else:
                    canvas.create_image(self.px-5,self.py+40,image=ImageTk.PhotoImage(bodyImg))
            headSprite = self.image.fireHeadSheets[self.headIndex]
             # this index will change in the future as more moves added
            headImg = headSprite[self.headSpriteCount[self.headIndex]]
            if self.headIndex == 0:
                canvas.create_image(self.px,self.py, image=ImageTk.PhotoImage(headImg))
            elif self.headIndex == 1:
                if self.dx < 0:
                    headImg = headImg.transpose(Image.FLIP_LEFT_RIGHT)
                    canvas.create_image(self.px+5,self.py+4, image=ImageTk.PhotoImage(headImg))
                else:
                    canvas.create_image(self.px-20,self.py+5, image=ImageTk.PhotoImage(headImg))
                
        else:
            bodySprite = self.image.waterBodySheets[self.bodyIndex]
            bodyImg = bodySprite[self.bodySpriteCount[self.bodyIndex]]
            if self.bodyIndex == 0:
                canvas.create_image(self.px-1,self.py+32, image=ImageTk.PhotoImage(bodyImg))
            elif self.bodyIndex == 1:
                if self.dx < 0:
                    bodyImg = bodyImg.transpose(Image.FLIP_LEFT_RIGHT)
                    canvas.create_image(self.px,self.py+40,image=ImageTk.PhotoImage(bodyImg))
                else:
                    canvas.create_image(self.px,self.py+40,image=ImageTk.PhotoImage(bodyImg))
            headSprite = self.image.waterHeadSheets[self.headIndex]
            headImg = headSprite[self.headSpriteCount[self.headIndex]]
            if self.headIndex == 0:
                canvas.create_image(self.px,self.py, image=ImageTk.PhotoImage(headImg))
            elif self.headIndex == 1:
                if self.dx < 0:
                    headImg = headImg.transpose(Image.FLIP_LEFT_RIGHT)
                    canvas.create_image(self.px+20,self.py, image=ImageTk.PhotoImage(headImg))
                else:
                    canvas.create_image(self.px-20,self.py, image=ImageTk.PhotoImage(headImg))


def charAppStarted(app):
    # called under appStarted in Main
    # initializes waterGirl and fireboy object and load image to it
    app.waterGirl = Character('water',80,560,spS.waterSprite)
    waterstill = app.loadImage('water1.png')
    stillbody = app.loadImage('waterBodyStill.png')
    waterrun = app.loadImage('waterrun.png')
    waterBodyRun = app.loadImage('waterBodyRun.png')
    spS.waterSprite.createWaterStill(app,waterstill)
    spS.waterSprite.createWaterBody(app,stillbody)
    spS.waterSprite.createWaterRun(app,waterrun)
    spS.waterSprite.createWaterBodyRun(app,waterBodyRun)
    app.waterGirl.image = spS.waterSprite

    # same as the previous section but for fireBoy object
    app.fireBoy = Character('fire', 80,660,spS.fireSprite)
    firestill = app.loadImage('firestill.png')
    firerun = app.loadImage('firerun.png')
    stillbody = app.loadImage('fireBodyStill.png')
    fireBodyRun = app.loadImage('fireBodyRun.png')
    spS.fireSprite.createFireStill(app,firestill)
    spS.fireSprite.createFireBody(app,stillbody)
    spS.fireSprite.createFireRun(app,firerun)
    spS.fireSprite.createFireBodyRun(app,fireBodyRun)
    app.fireBoy.image = spS.fireSprite


        


