from pygameSupport import PygameEnviroment as env
import pygame
import board

class game:
    blockSize = 60
    backgroundColor = (0, 0, 12)
    selectionColor = (255, 255, 255)


    def __init__(self, whiteSquareColor=(175, 29, 59), blackSquareColor=(77,70,70)):
        self.whiteSquareColor = whiteSquareColor
        self.blackSquareColor = blackSquareColor

        self.board = board.chessBoard(self)
        self.numHozBlocks = len(self.board.boardLayout[0])
        self.numVertBlocks = len(self.board.boardLayout[1])
        self.width = int(self.numHozBlocks * self.blockSize)
        self.height = int(self.numVertBlocks * self.blockSize)
        self.environment = env(self.width, self.height, 'chess')

        self.pieceTextures = self.createPieceTextures()
        self.refreshPieces()
        self.done = False
        self.positionSelected = None
        self.playerTurn = 0



    def createPieceTextures(self):
        pieceNames = ['Pawn', 'Rook', 'Knight', 'Bishop', 'Queen', 'King']
        colors = ['white', 'black']
        pieceTextures = self.environment.loadImages('pieces', [color+name for color in colors for name in pieceNames],
                                             '.png', (self.blockSize, self.blockSize))

        return pieceTextures


    def refreshPieces(self):
        self.environment.removeChildren()
        pieces = []
        for rowNum, row in enumerate(self.board.boardLayout):
            rowOfPieces = []
            for columnNum, block in enumerate(row):
                if block != 0:
                    textureNum = int((int(block) + (block - int(block)) * 2 * (len(self.pieceTextures)/2)) - 1)
                    chessTexture = self.pieceTextures[textureNum]
                    pieceLocation = ((rowNum * self.blockSize), (columnNum * self.blockSize))
                    piece = self.board.createNewPiece((rowNum, columnNum), chessTexture, pieceLocation, block)
                    rowOfPieces.append(piece)
                    self.environment.addChild(piece)
                else:
                    rowOfPieces.append(0)
            pieces.append(rowOfPieces)

        self.board.collectionOfPieces = pieces




    def updateGameScreen(self):
        self.environment.resetBackGround(allBackGround=True)
        self.drawBoard()
        self.environment.renderChildren()
        pygame.display.flip()


    def drawBoard(self):
        for rowNum, row in enumerate(self.board.boardLayout):
            for columnNum, block in enumerate(row):
                blockPostionInView = ((rowNum * self.blockSize), (columnNum * self.blockSize))
                blockRect = pygame.Rect(blockPostionInView, (self.blockSize, self.blockSize))
                if (rowNum + columnNum) % 2 == 0:
                    pygame.draw.rect(self.environment.display, self.whiteSquareColor, blockRect)
                elif (rowNum + columnNum) % 2 != 0:
                    pygame.draw.rect(self.environment.display, self.blackSquareColor, blockRect)

        if self.positionSelected:
            selectPos = (int(self.positionSelected[1] * self.blockSize),
                         int(self.positionSelected[0] * self.blockSize))
            selectRect = pygame.Rect(selectPos, (self.blockSize, self.blockSize))
            pygame.draw.rect(self.environment.display, self.selectionColor, selectRect, 5)



    def userMove(self, position):
        gridLocation = (int(position[1] / self.blockSize), int(position[0] / self.blockSize))
        locationType = self.board.boardLayout[(gridLocation[0], gridLocation[1])]
        if self.positionSelected:
            if self.board.checkForValidMove(self.positionSelected, gridLocation):
                self.refreshPieces()
                self.positionSelected = None
                self.swapTurns()
                self.updateGameScreen()
                return
            else:
                self.positionSelected = None


        if locationType != 0 and ((locationType - int(locationType))*2) == self.playerTurn:
            self.positionSelected = gridLocation

        self.updateGameScreen()

    def swapTurns(self):
        self.playerTurn = 0 if self.playerTurn == 1 else 1
        self.board.flipBoard()
        self.refreshPieces()



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

                if event.type == pygame.MOUSEBUTTONUP:
                    self.userMove(event.pos)



        self.environment.quit()


if __name__ == '__main__':
    newGame = game()
    newGame.run()



