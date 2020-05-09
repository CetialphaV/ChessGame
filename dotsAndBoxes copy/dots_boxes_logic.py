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
    posit_dict = {'u': 0, 'r': 1, 'd': 2, 'l': 3}
    posit_list = [2, 3, 5, 7]
    extra_list = [7, 3, 1, 5]
    for a in range(0, 8):
        X = int(np.floor(a/3) % 3)
        Y = a % 3
        try:
            if (row_box - X >= 0) and (col_box - Y >= 0):
                if a == 4:
                    board[row_box - X][col_box - Y] *= posit_list[posit_dict[position]] ** player
                elif a == extra_list[posit_dict[position]]:
                    board[row_box - X][col_box - Y] *= posit_list[(posit_dict[position]+2) % 4] ** player
                if (board[row_box - X][col_box - Y] % 210 == 0) and \
                        (board[row_box - X][col_box - Y] % 11 != 0) and \
                        (board[row_box - X][col_box - Y] % 13 != 0):
                    board[row_box - X][col_box - Y] *= (2*player + 9)
        except:
            continue
    return board

