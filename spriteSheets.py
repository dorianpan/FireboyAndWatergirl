from cmu_112_graphics import *

# spritesheets and graphs from: 
# https://github.com/RRCAT920/Fireboy-and-Watergirl/tree/master/assets

# class that contains all sprite animations for waterGirl
class WaterSprite(object):
    def __init__(self):
        self.waterHeadSheets = [] # list of water head animation
        self.waterBodySheets = [] # list of water body animation
        
    def createWaterStill(self,app,image):
        still = []
        for i in range(6):
            sprite = image.crop((25+134*i, 20, 100+134*i, 100))
            still.append(sprite)
        for i in range(4):
            sprite = image.crop((829+134*i, 23, 904+134*i, 103))
            still.append(sprite)
        for i in range(5):
            sprite = image.crop((4+134*i, 137, 79+134*i, 217))
            still.append(sprite)
        for i in range(6):
            sprite = image.crop((829+134*i, 134, 904+134*i, 214))
            still.append(sprite)
        for i in range(4):
            sprite = image.crop((23+134*i, 265, 98+134*i, 345))
            still.append(sprite)
        for i in range(5):
            sprite = image.crop((846+134*i, 253, 921+134*i, 333))
            still.append(sprite)
        self.waterHeadSheets.append(still)
    
    def createWaterRun(self,app,image):
        run = []
        for i in range(3):
            sprite = image.crop((22+178*i, 20, 122+178*i, 100))
            run.append(sprite)
        for i in range(3):
            sprite = image.crop((39+178*i, 263, 139+178*i, 343))
            run.append(sprite)
        for i in range(5):
            sprite = image.crop((16+178*i, 144, 116+178*i, 224))
            run.append(sprite)
        self.waterHeadSheets.append(run)
    
    def createWaterBody(self,app,image):
        body = []
        body.append(image)
        self.waterBodySheets.append(body)

    def createWaterBodyRun(self,app,image):
        run = []
        for i in range(4):
            sprite = image.crop((23+135*i, 20, 93+135*i, 100))
            run.append(sprite)
        for i in range(4):
            # sprite = image.crop((687+135*i, 30, 757+135*i, 110))
            sprite = image.crop((552+135*i, 30, 622+135*i, 110))
            run.append(sprite)
        self.waterBodySheets.append(run)
    



# class that contains all sprite animations for FireSprite
class FireSprite(object):
    def __init__(self):
        self.fireHeadSheets = [] # 2d list containing all the sprites
        self.fireBodySheets = []
    def createFireStill(self,app,image):
        still = []
        for i in range(6):
            sprite = image.crop((25+134*i, 20, 100+134*i, 100))
            still.append(sprite)
        for i in range(4):
            sprite = image.crop((834+134*i, 19, 909+134*i, 99))
            still.append(sprite)
        for i in range(5):
            sprite = image.crop((40+134*i, 139, 115+134*i, 219))
            still.append(sprite)
        for i in range(4):
            sprite = image.crop((831+134*i, 141, 906+134*i, 221))
            still.append(sprite)
        self.fireHeadSheets.append(still)

    def createFireRun(self,app,image):
        imgL = []
        sprite = image.crop((10, 20, 100, 100))
        imgL.append(sprite)
        for i in range(4):
            sprite = image.crop((12+160*i, 134, 102+160*i, 214))
            imgL.append(sprite)
        
        for i in range(4):
            sprite = image.crop((-1+160*i, 498, 89+160*i, 578))
            imgL.append(sprite)
        sprite = image.crop((20,257,110,337))
        imgL.append(sprite)
        sprite = image.crop((16,377,106,457))
        imgL.append(sprite)
        self.fireHeadSheets.append(imgL)

    def createFireBody(self,app,image):
        body = []
        body.append(image)
        self.fireBodySheets.append(body)
    
    def createFireBodyRun(self,app,image):
        run=[]
        for i in range(3):
            sprite = image.crop((23+135*i, 20, 93+135*i, 100))
            run.append(sprite)
        for i in range(4):
            sprite = image.crop((16+135*i, 140, 86+135*i, 220))
            run.append(sprite)
        sprite = image.crop((13, 261, 83, 341))
        run.append(sprite)
        self.fireBodySheets.append(run)

waterSprite = WaterSprite()
fireSprite = FireSprite()

        