from pygameSupport import PygameEnviroment as env
import pygame
from dots_boxes_logic import *


class game:
    blockSize = 60
    backgroundColor = (255, 226, 188)
    dotColor = (88, 180, 174)
    selectedDotColor = (255, 82, 0)
    lineColor = (250, 145, 145)
    textColor = (0, 0, 0)
    RENDEREVENT = pygame.USEREVENT + 1


    def __init__(self, aiPlaying=False):
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
        self.dotSelected = None
        self.aiPlaying = aiPlaying
        self.player1Score = 0
        self.player2Score = 0
        self.fontSize = int(self.dotSize * 1.5)



    def updateGameScreen(self):
        self.environment.resetBackGround(allBackGround=True)
        self.drawDots()
        self.drawLines()
        self.environment.renderChildren()
        self.displayScore()
        pygame.display.flip()


    def drawDots(self):
        for dotRowNum in range(self.numDots):
            for dotColumnNum in range(self.numDots):
                dotPostionX = self.screenBuffer + self.spaceBetweenDots * dotRowNum
                dotPostionY = self.screenBuffer + self.spaceBetweenDots * dotColumnNum
                dotPos = (dotPostionX, dotPostionY)

                if self.dotSelected and (dotRowNum == int(self.dotSelected[0])) and (dotColumnNum == int(self.dotSelected[1])):

                    pygame.draw.circle(self.environment.display, self.selectedDotColor, dotPos, self.dotSize)
                else:
                    pygame.draw.circle(self.environment.display, self.dotColor, dotPos, self.dotSize)


    def drawLines(self):
        for xLoc, row in enumerate(self.board):
            for yLoc, value in enumerate(row):
                self.drawLine((xLoc, yLoc), value)

    def message_display(self, text, pos, fontSize, bottomLeftAlignment=True):
        largeText = pygame.font.Font('freesansbold.ttf', fontSize)
        textSurface = largeText.render(text, True, self.textColor)
        textRect = textSurface.get_rect()
        if bottomLeftAlignment:
            textRect.bottomleft = pos
        else:
            textRect.bottomright = pos
        self.environment.display.blit(textSurface, textRect)

    def displayScore(self):
        self.message_display(f"Player 1 Score: {self.player1Score}", (int((self.screenBuffer * 2)), int(self.screenBuffer/2)), self.fontSize)
        self.message_display(f"Player 2 Score: {self.player1Score}", (int(self.size - self.screenBuffer * 2), int(self.screenBuffer / 2)), self.fontSize, False)


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
        xDotLoc = (location[0] - self.screenBuffer) / self.spaceBetweenDots
        yDotLoc = (location[1] - self.screenBuffer) / self.spaceBetweenDots
        if not self.dotSelected:
            self.dotSelected = (round(xDotLoc), round(yDotLoc))
        elif self.dotSelected == (round(xDotLoc), round(yDotLoc)):
            self.dotSelected = None
        else:
            secondDot = (round(xDotLoc), round(yDotLoc))
            moveDirection = self.checkForValidMove(self.dotSelected, secondDot)
            if moveDirection:
                if ((secondDot[0] < self.dotSelected[0]) and (moveDirection == 2)) or ((secondDot[1] < self.dotSelected[1]) and (moveDirection == 7)):
                    squarePos = (int(secondDot[0]), int(secondDot[1]))
                else:
                    squarePos = (int(self.dotSelected[0]), int(self.dotSelected[1]))
                self.playerMadeMove(squarePos, moveDirection)
                self.dotSelected = None
            else:
                self.dotSelected = None


    def playerMadeMove(self, location, moveType):
        if location[1] >= (self.numDots - 1):
            self.board[(location[0], location[1]-1)] = 5
        elif location[0] >= (self.numDots - 1):
            self.board[(location[0]-1, location[1])] = 3
        else:
            self.board[location] = moveType

        if self.playerTurn == 0:
            self.playerTurn = 1
        else:
            self.playerTurn = 0

    def checkForValidMove(self, dot1, dot2):
        moveDirection = None
        if (abs(dot1[0] - dot2[0]) == 1) and (dot1[1] == dot2[1]):
            moveDirection = 2
        elif (dot1[0] == dot2[0]) and (abs(dot1[1] - dot2[1]) == 1):
            moveDirection = 7


        return moveDirection


    def aiMakeMove(self, pos, move):
        pass

    def getState(self):
        pass


    def run(self):
        """
        This function is handles initial setup of the game and will begin the run loop of the game
        :return:
        """
        self.environment.runEnviroment()
        self.environment.backgroundColor = self.backgroundColor
        pygame.time.set_timer(self.RENDEREVENT, 200)

        self.updateGameScreen()

        while not self.done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

                if event.type == self.RENDEREVENT:
                    self.updateGameScreen()

                if event.type == pygame.MOUSEBUTTONDOWN and (not self.aiPlaying):
                    self.userClickedLocation(event.pos)


        self.environment.quit()


if __name__ == '__main__':
    newGame = game()
    newGame.run()



