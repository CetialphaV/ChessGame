from pygameSupport import Sprite


class Piece(Sprite):
    def __init__(self, boardLocation, typeNum, board, texture=None, location=(0, 0)):
        super().__init__(texture, location)
        self.boardLocation = boardLocation
        self.board = board
        self.typeNum = typeNum


class Pawn(Piece):

    def getValidMoves(self):
        moves = []
        print(self.typeNum)
        for rowNum, row in enumerate(self.board.boardLayout):
            for columnNum, block in enumerate(row):
                moves.append((rowNum, columnNum))
        return moves

class Knight(Piece):
    def getValidMoves(self):
        moves = []
        print(self.typeNum)
        for rowNum, row in enumerate(self.board.boardLayout):
            for columnNum, block in enumerate(row):
                moves.append((rowNum, columnNum))
        return moves

class King(Piece):
    def getValidMoves(self):
        moves = []
        print(self.typeNum)
        for rowNum, row in enumerate(self.board.boardLayout):
            for columnNum, block in enumerate(row):
                moves.append((rowNum, columnNum))
        return moves

class Bishop(Piece):
    def getValidMoves(self):
        moves = []
        print(self.typeNum)
        for rowNum, row in enumerate(self.board.boardLayout):
            for columnNum, block in enumerate(row):
                moves.append((rowNum, columnNum))
        return moves

class Queen(Piece):
    def getValidMoves(self):
        moves = []
        print(self.typeNum)
        for rowNum, row in enumerate(self.board.boardLayout):
            for columnNum, block in enumerate(row):
                moves.append((rowNum, columnNum))
        return moves

class Rook(Piece):
    def getValidMoves(self):
        moves = []
        print(self.typeNum)
        for rowNum, row in enumerate(self.board.boardLayout):
            for columnNum, block in enumerate(row):
                moves.append((rowNum, columnNum))
        return moves