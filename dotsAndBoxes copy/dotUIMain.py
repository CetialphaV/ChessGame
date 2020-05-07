from pygameSupport import PygameEnviroment as env
import pygame


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
        self.done = False
        self.positionSelected = None
        self.playerTurn = 0



    def updateGameScreen(self):
        self.environment.resetBackGround(allBackGround=True)
        self.drawBoard()
        self.environment.renderChildren()
        self.drawLine((0, 1), 5)
        pygame.display.flip()


    def drawBoard(self):
        for dotRowNum in range(self.numDots):
            for dotColumnNum in range(self.numDots):
                spaceBetweenDots = int((self.size - (self.screenBuffer * 2)) / (self.numDots-1))
                dotPostionX = self.screenBuffer + spaceBetweenDots * dotRowNum
                dotPostionY = self.screenBuffer + spaceBetweenDots * dotColumnNum
                pygame.draw.circle(self.environment.display, self.dotColor, (dotPostionX, dotPostionY), self.dotSize)


    def getDotsForLocation(self, location):
        spaceBetweenDots = int((self.size - (self.screenBuffer * 2)) / (self.numDots - 1))
        topLeft = ((location[0] * spaceBetweenDots + self.screenBuffer), location[1] * spaceBetweenDots + self.screenBuffer)
        topRight = (((location[0] + 1) * spaceBetweenDots + self.screenBuffer), location[1] * spaceBetweenDots + self.screenBuffer)
        bottomLeft = (((location[0]) * spaceBetweenDots + self.screenBuffer), (location[1] + 1) * spaceBetweenDots + self.screenBuffer)
        bottomRight = (((location[0] + 1) * spaceBetweenDots + self.screenBuffer), (location[1] + 1) * spaceBetweenDots + self.screenBuffer)
        dotLocations = {"topLeft": topLeft, "topRight": topRight, "bottomLeft": bottomLeft, "bottomRight": bottomRight}

        return dotLocations


    def drawLine(self, location, numToFactorize):
        dotLocations = self.getDotsForLocation(location)
        factorizedNums = [3, 5, 7,2]
        if 2 in factorizedNums:
            pygame.draw.line(self.environment.display, self.lineColor, dotLocations["topLeft"], dotLocations["topRight"], self.lineWidth)
        if 3 in factorizedNums:
            pygame.draw.line(self.environment.display, self.lineColor, dotLocations["topRight"], dotLocations["bottomRight"], self.lineWidth)
        if 5 in factorizedNums:
            pygame.draw.line(self.environment.display, self.lineColor, dotLocations["bottomLeft"], dotLocations["bottomRight"], self.lineWidth)
        if 7 in factorizedNums:
            pygame.draw.line(self.environment.display, self.lineColor, dotLocations["topLeft"], dotLocations["bottomLeft"], self.lineWidth)



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





        self.environment.quit()


if __name__ == '__main__':
    newGame = game()
    newGame.run()



