from cmu_112_graphics import *
import character as ca
import backGround as bg
import obstacle as ob
import maze as mz
NORTH = (0,-1)
SOUTH = (0,1)
WEST = (-1,0)
EAST = (1,0)
# spritesheets, graphs and title image from: 
# https://github.com/RRCAT920/Fireboy-and-Watergirl/tree/master/assets
# cannon image from:
# https://opengameart.org/content/tower-defence-basic-towers
# door image from:
# https://github.com/ZiadElGafy/Fireboy-And-Watergirl/tree/master/assets/graphics
# background forest image from:
# https://www.bing.com/images/search?view=detailV2&ccid=kXMqh%2bf6&id=
# 789468376AB35929E918FEA7D73E1BCA4495BB4A&thid=OIP.kXMqh-f6emEUqpmnHdrRqgHaEt&
# mediaurl=https%3a%2f%2fimg00.deviantart.net%2f56f7%2fi%2f2015%2f302%2ff%2f5%2fba
# sic_2d_forest_background_by_sonnysketch-d9eujn7.png&cdnurl=https%3a%2f%2fth.bing.
# com%2fth%2fid%2fR.91732a87e7fa7a6114aa99a71ddad1aa%3frik%3dSruVRMobPten%252fg%26p
# id%3dImgRaw%26r%3d0&exph=651&expw=1024&q=game+forest+
# background&simid=608016955187872241&FORM=IRPRST&ck=34C3D5406539
# 2773BE0EEC7A9E2B7D63&selectedIndex=108&ajaxhist=0&ajaxserp=0

########################################
## splash screen mode
########################################

# draws menu
def splashScreenMode_redrawAll(app,canvas):
    canvas.create_image(600,400,image= app.splashBackGround)
    bg.drawIconsInSplash(app,canvas)
    bg.drawImage(app,canvas)
    bg.drawCharacter(app,canvas)

def splashScreenMode_timerFired(app):
   bg.splashTimer(app)

def splashScreenMode_mouseMoved(app,event):
    bg.splashMouseMoved(app,event)

def splashScreenMode_mousePressed(app,event):
    bg.splashMousePressed(app,event)

#######################################
## help mode
########################################
# draws helper text and menu
def helpMode_redrawAll(app,canvas):
    bg.drawTextInHelp(app,canvas)
    bg.drawIconInHelp(app,canvas)


def helpMode_timerFired(app):
    if app.iconsPressed[3] == True: # back icon is pressed
        app.iconsPressed[3] = False # resets icon
        app.mode = 'splashScreenMode'
           
def helpMode_mouseMoved(app,event):
    bg.helpMouseMoved(app,event)

def helpMode_mousePressed(app,event):
   bg.helpMousePressed(app,event)


####################################
## game mode
####################################

def gameMode_timerFired(app):
    app.counter += 1
    # bg.gameModeTimer(app) # checks if icon pressed
    if app.gameLevel == 'Level 1':
        if app.gameClear == False and app.gameOver == False:
            app.waterGirl.timeRuns() # moves characters according to its dx,dy
            app.fireBoy.timeRuns() # same things as above
            app.level1Floors.checkOnFloor(app) # checks if characters are on floors
            app.level1Ceilings.checkHitCeiling(app) # checks if characters hit ceilings
            app.level1Walls.checkHitWalls(app) # checks if characters hit walls
            app.level1Floors.floorTimer1() # timer for the floating floor
            app.level1Floors.checkLevel1Button() # elevator that respond to button press
            bg.checkPressedTimer(app) # checks if button is pressed
            ob.generateBullet(app) # generates and moves bullets
            ob.checkGameClear(app) # checks if game is clear
            if not app.testing:
                ob.poolGameOver(app) # checks if character falls into the pool
    elif app.gameLevel == 'Level 2':
        if app.gameClear == False and app.gameOver == False:
            app.waterGirl.timeRuns() # moves characters according to its dx,dy
            app.fireBoy.timeRuns() # same things as above
            app.level2Floors.checkOnFloor(app) # checks if characters are on floors
            app.level2Ceilings.checkHitCeiling(app) # checks if characters hit ceilings
            app.level2Walls.checkHitWalls(app) # checks if characters hit walls
            app.level2Floors.floorTimer2() # timer for the floating panel
            app.level2Walls.checkLevel2Wall() # checks if button is pressed so
                                            #  the vertical wall could be lifted
            app.level2Floors.checkLevel2Button() # elevator that respond to button press
            bg.checkPressedTimer(app) # checks if button is pressed
            ob.generateBullet(app) # generates and moves bullets
            ob.checkGameClear(app) # checks if game is clear
            if not app.testing:
                ob.poolGameOver(app) # checks if character falls into the pool
    elif app.gameLevel == 'Maze':
        mz.mazeTimerFired(app) 
    for i in range(7,10):
        if app.iconsPressed[i] == True:
            start(app) # if "back" icon pressed under gameMode, restrat the game

# respond to key inputs
def gameMode_keyPressed(app,event):
    if app.gameLevel == 'Level 1' or app.gameLevel == 'Level 2':
        if app.gameOver == False and app.gameClear == False:
            app.waterGirl.move(event) 
            app.fireBoy.move(event) # checks key press inputs
        if event.key == 'r':
            ca.charAppStarted(app)
            app.gameOver = False
            app.gameClear = False
            app.counter = 0
        if event.key == 't':
            app.testing = not app.testing # for testing convenience
    elif app.gameLevel == 'Maze':
        mz.mazeKeyPressed(app,event)

# respond to key release
def gameMode_keyReleased(app,event):
    if app.gameLevel == 'Level 1' or 'Level 2':
        if app.gameOver == False and app.gameClear == False:
            app.waterGirl.keyReleased(event)
            app.fireBoy.keyReleased(event) # checks key release inputs

def gameMode_mouseMoved(app,event):
    bg.gameModeMouseMoved(app,event) # checks if mouse moved to icons

def gameMode_mousePressed(app,event):
    bg.gameModeMousePressed(app,event) # checks if mouse pressed icons

def gameMode_redrawAll(app,canvas):
    # draws everytings
    # canvas.create_rectangle(0,0,1200,750,fill='black')
    canvas.create_image(600,375,image = app.backGround)
    if app.gameLevel == 'Level 1':
        ob.drawDoors(app,canvas)
        app.waterGirl.drawCharacter(app,canvas)
        app.fireBoy.drawCharacter(app,canvas)
        ob.drawPools(app,canvas)
        app.level1Floors.drawFloor(app,canvas)
        app.level1Ceilings.drawCeiling(app,canvas) 
        app.level1Walls.drawWalls(app,canvas)
        for button in app.level1Floors.buttons:
            button.drawButton(canvas)
        canvas.create_image(1100,250,anchor = 'se',image = app.cannon)
        ob.drawBullet(app,canvas)
        if app.gameOver:
            canvas.create_text(600,400,text='       GameOver\nPress r to restart',
                        font = 'Algerian 50 bold',fill='orangered')
        if app.gameClear:
            canvas.create_text(600,400,text='       Game Clear\nPress r to restart',
                        font = 'Algerian 50 bold',fill='cyan')
        canvas.create_text(430,50,text = 'press t to turn on/off test mode\nin test mode player will be invincible',
                        font = 'Arial 18 bold',fill = 'yellow')
        if app.testing:
            canvas.create_text(430,90,text='Test mode: On',font = 'Arial 18 bold',
                            fill = 'green')
        else:
            canvas.create_text(430,90,text='Test mode: Off',font = 'Arial 18 bold',
                            fill = 'red')

    elif app.gameLevel == 'Level 2' :
        ob.drawDoors(app,canvas)
        ob.drawPools(app,canvas)
        app.waterGirl.drawCharacter(app,canvas)
        app.fireBoy.drawCharacter(app,canvas)
        app.level2Floors.drawFloor(app,canvas)
        app.level2Ceilings.drawCeiling(app,canvas) 
        app.level2Walls.drawWalls(app,canvas)
        canvas.create_image(1000,150,anchor = 'se',image = app.cannon)
        for button in app.level2Floors.buttons:
            button.drawButton(canvas)
        ob.drawBullet(app,canvas)
        if app.gameOver:
            canvas.create_text(600,400,text='       GameOver\nPress r to restart',
                        font = 'Algerian 50 bold',fill='orangered')
        if app.gameClear:
            canvas.create_text(600,400,text='       Game Clear\nPress r to restart',
                        font = 'Algerian 50 bold',fill='cyan')
        canvas.create_text(430,50,text = 'press t to turn on/off test mode\nin test mode player will be invincible',
                        font = 'Arial 18 bold',fill = 'yellow')
        if app.testing:
            canvas.create_text(430,90,text='Test mode: On',font = 'Arial 18 bold',
                            fill = 'green')
        else:
            canvas.create_text(430,90,text='Test mode: Off',font = 'Arial 18 bold',
                            fill = 'red')
    elif app.gameLevel == 'Maze':
        mz.mazeRedrawAll(app,canvas)
    bg.drawIconsInGameMode(app,canvas)

       



##############################
## appStarted Part
##############################
def appStarted(app):
    start(app)

def start(app):
    bg.mapLevel1Floor.runAppLevel1(app) # app.level1Floors object
    bg.mapLevel1Ceilings.runAppLevel1(app) # app.ceilings object
    bg.mapLevel1Walls.runAppLevel1(app) # app.walls object
    ###### Level 2 ######
    bg.mapLevel2Floor.runAppLevel2(app) # app.level2Floors object
    bg.mapLevel2Ceilings.runAppLevel2(app) # app.ceilings object
    bg.mapLevel2Walls.runAppLevel2(app) # app.walls object
    bg.createSplashScreenIcons(app) # app.icons, app.iconsOn,app.iconsPressed, app.iconsColor
    app.splashBackGround = ImageTk.PhotoImage(app.loadImage('TempleHall.png'))
    app.backGround = ImageTk.PhotoImage(app.scaleImage(app.loadImage('forestBackGround.png'),3/2))
    app.counter = 0
    app.gameOver = False
    app.gameClear = False
    app.levelScreen = False
    app.gameLevel = ''
    app.title = app.scaleImage(app.loadImage('title.png'),4/3)
    app.cannon = ImageTk.PhotoImage(app.scaleImage(app.loadImage('Cannon.png'),0.3))
    app.fireDoor = app.scaleImage(app.loadImage('doorFire.png'),0.7)
    app.waterDoor = app.scaleImage(app.loadImage('doorWater.png'),0.7)
    app.mode = 'splashScreenMode'
    ob.bulletAppStarted(app)
    ob.doorAppStartedLevel1(app)
    ob.doorAppStartedLevel2(app)
    ob.poolAppStartedLevel1(app)
    ob.poolAppStartedLevel2(app)
    mz.mazeAppStarted(app)
    ca.charAppStarted(app)
    app.testing = False



runApp(width=1200, height=750)