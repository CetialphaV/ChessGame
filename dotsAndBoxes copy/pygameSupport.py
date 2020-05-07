import pygame
import sys
import numpy as np



class Sprite:


    def __init__(self, texture=None, location=(0, 0)):
        self.texture = texture
        self.children = []
        self.canMove = True
        self.movementDirection = None
        self.previousDirection = None
        self.name = ''
        self.animationImages = []
        self.animationTimer = 0
        self.animationSwapTime = 0
        self.animationIndex = 0
        self.rect = None
        self.hasAnimation = False
        self.shouldUpdate = True
        self.previousRect = None

        if self.texture is not None:
            self.createRect(location)
        else:
            self.initiallocation = location

    def addChild(self, sprite):
        """
        This function adds a sprite as a child to another sprite. A sprite that is a child of another sprite
        can have its animation/texture updated by calls to the environment to render childSprites.
        :param sprite: Sprite
        :return: None
        """
        self.children.append(sprite)

    def removeChildren(self):
        self.children = []

    def loadImages(self, directoryName, imageNames, fileType, size=None):
        """
        Loads images from a directory. Loads the images into a list.
        :param directoryName: String
        :param imageNames: list
        :param fileType: String
        :param size: Tuple
        :return: list
        """
        Images = []
        for imageName in imageNames:
            modifiedName = directoryName + '/' + imageName + fileType
            image = pygame.image.load(modifiedName)
            if size:
                image = pygame.transform.scale(image, size).convert_alpha()
            Images.append(image)
        return Images

    def createRect(self, location):
        """
        Creates a pygame rect from the sprite's texture and sets it to the sprite's location.
        :param location:
        :return:
        """
        self.rect = self.texture.get_rect()
        self.rect.y = location[0]
        self.rect.x = location[1]
        self.previousRect = self.rect

    def neighborBlocks(self, blockCoordinates, maze):
        x = blockCoordinates[0]
        y = blockCoordinates[1]
        neighbors = {}
        if x - 1 >= 0:
            neighbors['Up'] = ((x - 1), y)
        else:
            neighbors["Up"] = None
        if y - 1 >= 0:
            neighbors['Left'] = (x, (y - 1))
        else:
            neighbors['Left'] = None
        if x + 1 <= (maze.shape[0] - 1):
            neighbors["Down"] = ((x + 1), y)
        else:
            neighbors["Down"] = None
        if y + 1 <= (maze.shape[1] - 1):
            neighbors['Right'] = (x, (y + 1))
        else:
            neighbors['Right'] = None

        return neighbors

    def loadAnimation(self, images, numberOfFramesPerSwap):
        self.animationIndex = 0
        self.texture = images[self.animationIndex]
        self.animationImages = images
        self.animationTimer = 0
        self.animationSwapTime = numberOfFramesPerSwap
        self.hasAnimation = True

        if self.rect is None:
            self.createRect(self.initiallocation)

    def updateAnimation(self):
        if self.animationTimer % self.animationSwapTime == 0:
            if self.animationIndex >= (len(self.animationImages) - 1):
                self.animationIndex = 0
            else:
                self.animationIndex += 1

            self.texture = self.animationImages[self.animationIndex]

        self.animationTimer += 1

    def moveSprite(self):
        """
        Override to create movement for any sprite object.
        This method does not move the Sprite on its own. Be sure to call the super class method before implementing
        custom move mechanics for the sprite. This function takes care of background tasks to make rendering more efficient.
        :return:
        """
        self.previousRect = self.rect.copy()



class PygameEnviroment(Sprite):
    gravity = 1
    done = False
    backgroundColor = None
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)

    def __init__(self, width, height, displayText):
        super().__init__()
        self.displayText = displayText
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.width, self.height))

    def quit(self):
        self.done = True
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def updateGravity(self):
        for child in self.children:
            child.y -= self.gravity

    def resetBackGround(self, allBackGround = True, rectToFill = None):
        if self.backgroundColor:
            if allBackGround:
                self.display.fill(self.backgroundColor)
            else:
                self.display.fill(self.backgroundColor, rect=rectToFill)

    def renderChildren(self, shouldUpdateView=False):
        rectsToUpdate = []

        for child in self.children:
            if child.shouldUpdate:

                self.display.blit(child.texture, child.rect)
                rectsToUpdate.append(child.rect)

        #if shouldUpdateView:
        pygame.display.update(rectsToUpdate)


    def renderChild(self, sprite):
        self.display.blit(sprite.texture, sprite.rect)
        pygame.display.update(sprite)

    def renderSpriteArray(self, spriteArray):
        for sprite in spriteArray:
            self.display.blit(sprite.texture, sprite.rect)
        pygame.display.update(spriteArray)

    def runEnviroment(self):
        pygame.init()
        pygame.display.set_caption(self.displayText)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def playBackgroundMusic(self, name, volume=0.5):
        pygame.mixer.music.load(name + '.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)

    def playSoundEffect(self, name, volume=0.5):
        sound = pygame.mixer.Sound(name + '.wav')
        sound.set_volume(volume)
        pygame.mixer.Sound.play(sound)

    def updateAnimations(self):
        for spite in self.children:
            if spite.hasAnimation:
                spite.updateAnimation()




def loadMap(name):
    gameMap = np.genfromtxt(name, delimiter=', ', dtype=np.float)
    return gameMap

def saveMap(name, map):
    with open(name, 'w') as levelMap:
        for row in map:
            newLine = ''
            for block in row:
                newLine += str(block) + ', '

            newLine = newLine[:(len(newLine) - 2)]
            newLine += '\n'
            levelMap.write(newLine)
