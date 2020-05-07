from pygameSupport import PygameEnviroment as env
import pygame


class game:
    blockSize = 60
    backgroundColor = (255, 255, 255)
    selectionColor = (255, 255, 255)


    def __init__(self, whiteSquareColor=(175, 29, 59), blackSquareColor=(77,70,70)):
        self.whiteSquareColor = whiteSquareColor
        self.blackSquareColor = blackSquareColor

        self.numDots = 20
        self.screenMuliplier = 30
        self.size = self.numDots * self.screenMuliplier
        self.environment = env(self.size, self.size, 'chess')
        self.screenBuffer = int(self.size / 8)
        self.dotSize = 8

        self.done = False
        self.positionSelected = None
        self.playerTurn = 0


    def updateGameScreen(self):
        self.environment.resetBackGround(allBackGround=True)
        self.drawBoard()
        self.environment.renderChildren()
        pygame.display.flip()


    def drawBoard(self):
        # for rowNum, row in enumerate((num)):
        #     for columnNum, block in enumerate(row):
        #         blockPostionInView = ((rowNum * self.blockSize), (columnNum * self.blockSize))
        #         blockRect = pygame.Rect(blockPostionInView, (self.blockSize, self.blockSize))
        #         if (rowNum + columnNum) % 2 == 0:
        #             pygame.draw.rect(self.environment.display, self.whiteSquareColor, blockRect)
        #         elif (rowNum + columnNum) % 2 != 0:
        #             pygame.draw.rect(self.environment.display, self.blackSquareColor, blockRect)


        for dotRowNum in range(self.numDots):
            for dotColumnNum in range(self.numDots):
                spaceBetweenDots = int((self.size - (self.screenBuffer * 2)) / self.numDots)
                dotPostionX = self.screenBuffer + spaceBetweenDots * dotRowNum
                dotPostionY = self.screenBuffer + spaceBetweenDots * dotColumnNum
                print(dotPostionX, dotPostionY)
                pygame.draw.circle(self.environment.display, self.environment.RED, (dotPostionX, dotPostionY), self.dotSize)










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



