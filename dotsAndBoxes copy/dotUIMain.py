from pygameSupport import PygameEnviroment as env
import pygame
from math import ceil
from dots_boxes_logic import *


class game:
    blockSize = 60
    backgroundColor = (255, 226, 188)
    dotColor = (88, 180, 174)
    lineColor = (250, 145, 145)


    def __init__(self):
        self.numDots = 10
        self.screenMuliplier = 40
        self.size = self.numDots * self.screenMuliplier
        self.environment = env(self.size, self.size, 'DotsAndBoxes')
        self.screenBuffer = int(self.size / 12)
        self.dotSize = 8
        self.dotBuffer = self.dotSize * 4
        self.lineWidth = int(self.dotSize * 0.75)
        self.spaceBetweenDots = int((self.size - (self.screenBuffer * 2)) / (self.numDots - 1))
        self.done = False
        self.positionSelected = None
        self.playerTurn = 0
        self.board = board_maker(self.numDots, self.numDots)
        self.board[0][0] = 2
        self.board[1][8] = 7



    def updateGameScreen(self):
        self.environment.resetBackGround(allBackGround=True)
        self.drawDots()
        self.drawLines()
        self.environment.renderChildren()
        pygame.display.flip()


    def drawDots(self):
        for dotRowNum in range(self.numDots):
            for dotColumnNum in range(self.numDots):
                dotPostionX = self.screenBuffer + self.spaceBetweenDots * dotRowNum
                dotPostionY = self.screenBuffer + self.spaceBetweenDots * dotColumnNum
                pygame.draw.circle(self.environment.display, self.dotColor, (dotPostionX, dotPostionY), self.dotSize)


    def drawLines(self):
        for xLoc, row in enumerate(self.board):
            for yLoc, value in enumerate(row):
                self.drawLine((xLoc, yLoc), value)


    def getDotsForLocation(self, location):
        topLeft = ((location[0] * self.spaceBetweenDots + self.screenBuffer), location[1] * self.spaceBetweenDots + self.screenBuffer)
        topRight = (((location[0] + 1) * self.spaceBetweenDots + self.screenBuffer), location[1] * self.spaceBetweenDots + self.screenBuffer)
        bottomLeft = (((location[0]) * self.spaceBetweenDots + self.screenBuffer), (location[1] + 1) * self.spaceBetweenDots + self.screenBuffer)
        bottomRight = (((location[0] + 1) * self.spaceBetweenDots + self.screenBuffer), (location[1] + 1) * self.spaceBetweenDots + self.screenBuffer)
        dotLocations = {"topLeft": topLeft, "topRight": topRight, "bottomLeft": bottomLeft, "bottomRight": bottomRight}

        return dotLocations


    def drawLine(self, location, numToFactorize):
        dotLocations = self.getDotsForLocation(location)
        factorizedNums = [numToFactorize]
        if 2 in factorizedNums:
            pygame.draw.line(self.environment.display, self.lineColor, dotLocations["topLeft"], dotLocations["topRight"], self.lineWidth)
        if 3 in factorizedNums:
            pygame.draw.line(self.environment.display, self.lineColor, dotLocations["topRight"], dotLocations["bottomRight"], self.lineWidth)
        if 5 in factorizedNums:
            pygame.draw.line(self.environment.display, self.lineColor, dotLocations["bottomLeft"], dotLocations["bottomRight"], self.lineWidth)
        if 7 in factorizedNums:
            pygame.draw.line(self.environment.display, self.lineColor, dotLocations["topLeft"], dotLocations["bottomLeft"], self.lineWidth)

    def userClickedLocation(self, location):
        xDotLoc1 = int((location[0] - self.screenBuffer) / self.spaceBetweenDots)
        yDotLoc1 = int((location[1] - self.screenBuffer) / self.spaceBetweenDots)
        xDotLoc2 = ceil((location[0] - self.screenBuffer) / self.spaceBetweenDots)
        yDorLoc2 = ceil((location[1] - self.screenBuffer) / self.spaceBetweenDots)
        squareLoc = (xDotLoc1, yDotLoc1)
        direction = 0
        if xDotLoc1 < xDotLoc2:
            print("Top")
            print("Bottom")





    def run(self):
        """
        This function is handles initial setup of the game and will begin the run loop of the game
        :return:
        """
        self.environment.runEnviroment()
        self.environment.backgroundColor = self.backgroundColor


        self.updateGameScreen()

        while not self.done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.userClickedLocation(event.pos)





        self.environment.quit()


if __name__ == '__main__':
    newGame = game()
    newGame.run()



