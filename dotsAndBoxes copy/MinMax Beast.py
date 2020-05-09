import numpy as np
from dots_boxes_logic import *
import random as r

def rand(board):
    global rand_row, rand_posit, rand_col
    dict = {1: 'u', 2: 'r', 3: 'd', 4: 'l'}
    posit_dict = {'u': 2, 'r': 3, 'd': 5, 'l': 7}
    valid = False
    while (valid == False):
        rand_posit = dict[r.randint(1, 4)]
        max = np.shape(board)
        rand_row = r.randint(1, max[0])
        rand_col = r.randint(1, max[1])
        if board[rand_row-1][rand_col-1] % posit_dict[rand_posit] != 0:
            valid = True
    return rand_posit, rand_row, rand_col

def poss_scores(board, num):
    moves = []
    score = []
    for alt in range(num): # number of alternate moves tried
        temp_board = np.copy(board)
        player = 2
        change_player = True
        first = True
        tach = 0
        while sum(np.ravel(np.copy(temp_board) % 210) != 0):
            tach += 1
            if tach == r.randint(0, 5):
                break
            if change_player == True:
                if player == 2:
                    player = 1
                else:
                    player = 2
            pre_score = points(temp_board)
            guess = rand(temp_board)
            if first == True:
                moves.append(guess)
            first = False
            board_edit(temp_board, guess[0], player, guess[1], guess[2])
            fin_score = points(temp_board)
            if pre_score != fin_score:
                change_player = False
            else:
                change_player = True
        point = points(temp_board)
        score.append(point[1])
    return moves, score

def minimizer(moves, scores):
    uniq_mov = list(dict.fromkeys(moves))
    uniq_score = []
    for a in range(len(uniq_mov)):
        temp_score = []
        for b in range(len(moves)):
            if uniq_mov[a] == moves[b]:
                temp_score.append(scores[b])
        uniq_score.append(np.average(temp_score))
    final_move = uniq_mov[uniq_score.index(min(uniq_score))]
    print(uniq_mov)
    print(uniq_score)
    return final_move

def box_boy(board, num_alt_moves):
    a, b = poss_scores(board, num_alt_moves)
    move = minimizer(a, b)
    return move

board = [[2, 5*2, 3], [7*3, 210*13, 7*5]]
#print(rand(board))
print(box_boy(board, 500))





