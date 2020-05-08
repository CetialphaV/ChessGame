from pygameSupport import PygameEnviroment as env
import pygame
from dots_boxes_logic import *


class game:
    blockSize = 60
    backgroundColor = (255, 226, 188)
    dotColor = (88, 180, 174)
    selectedDotColor = (255, 82, 0)
    lineColorOne = (250, 145, 145)
    lineColorTwo = (122, 213, 124)
    textColor = (0, 0, 0)
    playerColors = [(187, 59, 14), (22, 36, 71)]
    RENDEREVENT = pygame.USEREVENT + 1


    def __init__(self, aiPlaying=False):
        self.numDots = 12
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
        self.playerTurn = 1
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
        self.displayScoreAndTurn()
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
        squareNotDivisibleBy210 = True
        for xLoc, row in enumerate(self.board):
            for yLoc, value in enumerate(row):
                self.drawLine((yLoc, xLoc), value)
                if value % 210 != 0:
                    squareNotDivisibleBy210 = False

        self.done = squareNotDivisibleBy210

    def message_display(self, text, pos, fontSize, bottomLeftAlignment=True, centerAlignment=False):
        largeText = pygame.font.Font('freesansbold.ttf', fontSize)
        textSurface = largeText.render(text, True, self.textColor)
        textRect = textSurface.get_rect()
        if bottomLeftAlignment:
            textRect.bottomleft = pos
        elif centerAlignment:
            textRect.center = pos
        else:
            textRect.bottomright = pos
        self.environment.display.blit(textSurface, textRect)

    def displayScoreAndTurn(self):

        self.message_display(f"Player 1 Score: {self.player1Score}", (int((self.screenBuffer * 2)), int(self.screenBuffer/2)), self.fontSize)
        self.message_display(f"Player 2 Score: {self.player2Score}", (int(self.size - self.screenBuffer * 2), int(self.screenBuffer / 2)), self.fontSize, False)
        self.message_display(f"Player Turn: {self.playerTurn}", (int(self.size/2), int(self.size - self.screenBuffer/2)), self.fontSize, False,  centerAlignment=True)


    def getDotsForLocation(self, location):
        topLeft = ((location[0] * self.spaceBetweenDots + self.screenBuffer), location[1] * self.spaceBetweenDots + self.screenBuffer)
        topRight = (((location[0] + 1) * self.spaceBetweenDots + self.screenBuffer), location[1] * self.spaceBetweenDots + self.screenBuffer)
        bottomLeft = (((location[0]) * self.spaceBetweenDots + self.screenBuffer), (location[1] + 1) * self.spaceBetweenDots + self.screenBuffer)
        bottomRight = (((location[0] + 1) * self.spaceBetweenDots + self.screenBuffer), (location[1] + 1) * self.spaceBetweenDots + self.screenBuffer)
        dotLocations = {"topLeft": topLeft, "topRight": topRight, "bottomLeft": bottomLeft, "bottomRight": bottomRight}

        return dotLocations


    def drawLine(self, location, numToFactorize):
        dotLocations = self.getDotsForLocation(location)
        if numToFactorize % 2 == 0:
            if (numToFactorize/2) % 2 == 0:
                lineColor = self.lineColorOne
            else:
                lineColor = self.lineColorTwo
            pygame.draw.line(self.environment.display, lineColor, dotLocations["topLeft"], dotLocations["topRight"], self.lineWidth)
        if numToFactorize % 3 == 0:
            if (numToFactorize/3) % 3 == 0:
                lineColor = self.lineColorOne
            else:
                lineColor = self.lineColorTwo
            pygame.draw.line(self.environment.display, lineColor, dotLocations["topRight"], dotLocations["bottomRight"], self.lineWidth)
        if numToFactorize % 5 == 0:
            if (numToFactorize/5) % 5 == 0:
                lineColor = self.lineColorOne
            else:
                lineColor = self.lineColorTwo
            pygame.draw.line(self.environment.display, lineColor, dotLocations["bottomLeft"], dotLocations["bottomRight"], self.lineWidth)
        if numToFactorize % 7 == 0:
            if (numToFactorize/7) % 7 == 0:
                lineColor = self.lineColorOne
            else:
                lineColor = self.lineColorTwo
            pygame.draw.line(self.environment.display, lineColor, dotLocations["topLeft"], dotLocations["bottomLeft"], self.lineWidth)


        if self.board[location] % 11 == 0:
            pygame.draw.rect(self.environment.display, self.playerColors[1], ((int(dotLocations['topLeft'][1] + self.dotSize/2),
                                                                               int(dotLocations['topLeft'][0] + self.dotSize/2)),
                                                                              (self.spaceBetweenDots  * 0.9, self.spaceBetweenDots * 0.9)))
        if self.board[location] % 13 == 0:
            pygame.draw.rect(self.environment.display, self.playerColors[0],
                             ((int(dotLocations['topLeft'][1] + self.dotSize / 2),
                               int(dotLocations['topLeft'][0] + self.dotSize / 2)),
                              (self.spaceBetweenDots * 0.9, self.spaceBetweenDots * 0.9)))

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


    def convertNumToLetter(self, num):
        if num == 2:
            return"u"
        elif num == 3:
            return "r"
        elif num == 5:
            return "d"
        elif num  == 7:
            return "l"

    def playerMadeMove(self, location, moveType):
        oldScores = [self.player1Score, self.player2Score]
        if location[1] >= (self.numDots - 1):
            if self.board[(location[1]-1, location[0])] % 5 == 0:
                return
            board_edit(self.board, (self.convertNumToLetter(5)), self.playerTurn, location[1], location[0]+1)
        elif location[0] >= (self.numDots - 1):
            if self.board[(location[1], location[0]-1)] % moveType == 3:
                return
            board_edit(self.board, (self.convertNumToLetter(3)), self.playerTurn, location[1]+1, location[0])
        else:
            if self.board[(location[1], location[0])] % moveType == 0:
                return
            board_edit(self.board, (self.convertNumToLetter(moveType)), self.playerTurn, location[1]+1, location[0]+1)

        pointValues = points(self.board)
        self.player1Score = pointValues[0]
        self.player2Score = pointValues[1]

        newScores = [self.player1Score, self.player2Score]

        if oldScores[0] == newScores[0] and oldScores[1] == newScores[1]:
            if self.playerTurn == 1:
                self.playerTurn = 2
            else:
                self.playerTurn = 1



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
        self.environment.playBackgroundMusic("backgroundMusic", 10)
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



