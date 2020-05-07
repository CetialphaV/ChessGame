from pygameSupport import loadMap
import numpy as np
from pieces import *


class chessBoard:
    def __init__(self, game=None):
        self.game = game
        self.boardLayout = loadMap('basicLayout')
        self.collectionOfPieces = []


    def checkForValidMove(self, posInit, posFinal):
        initialPiece = self.collectionOfPieces[posInit[0]][posInit[1]]
        validMoves = initialPiece.getValidMoves()


        if posFinal in validMoves:
            self.boardLayout[posInit] = 0
            self.boardLayout[posFinal] = initialPiece.typeNum
            return True
        else:
            return False


    def flipBoard(self):
        self.boardLayout = np.flip(self.boardLayout)

    def createNewPiece(self, boardLocation, texture, location, typeID):

        if int(typeID) == 2:
            newPiece = Rook(board=self, boardLocation=boardLocation, texture=texture, location=location, typeNum=typeID)
        elif int(typeID) == 3:
            newPiece = Knight(board=self, boardLocation=boardLocation, texture=texture, location=location, typeNum=typeID)
        elif int(typeID) == 4:
            newPiece = Bishop(board=self, boardLocation=boardLocation, texture=texture, location=location, typeNum=typeID)
        elif int(typeID) == 5:
            newPiece = Queen(board=self, boardLocation=boardLocation, texture=texture, location=location, typeNum=typeID)
        elif int(typeID) == 6:
            newPiece = King(board=self, boardLocation=boardLocation, texture=texture, location=location, typeNum=typeID)
        else:
            newPiece = Pawn(board=self, boardLocation=boardLocation, texture=texture, location=location, typeNum=typeID)


        return newPiece