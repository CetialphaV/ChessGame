import numpy as np

# Up - 2, Right - 3, Down - 5, Left - 7
# Player 1 - 11, Player 2 - 13

def points(board):
    """
    :param board: Enter board with encoded values
    :return: Returns the points of player 1 and 2
    """
    p1_pts = np.count_nonzero(board % 11 == 0)
    p2_pts = np.count_nonzero(board % 13 == 0)
    return p1_pts, p2_pts

def board_maker(rows, col):
    """
    :param rows: Enter number of rows of dots (not boxes)
    :param col: Enter number of columns of dots (not boxes)
    :return: Returns a board with rows and columns of boxes (not dots)
    """
    board = np.ones([rows-1, col-1])
    return board

def board_edit(board, position, player, row_box, col_box):
    """
    :param board: Enter the board with encoded values
    :param position: Enter the position (u, r, d, l)
    :param player: Enter the player currently moving (1, 2)
    :param row_box: Enter the row of the value to be added
    :param col_box: Enter the column of the value to be added
    :return: Returns the edited board
    """
    posit_dict = {'u': 2, 'r': 3, 'd': 5, 'l': 7}
    board[row_box-1][col_box-1] *= posit_dict[position]
    if board[row_box-1][col_box-1] % 210 == 0:
        board[row_box-1][col_box-1] *= (9 + 2 * player)
    return board





