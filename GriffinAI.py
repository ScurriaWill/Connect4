import random


def return_move(board, num_win):
    return random.randint(0, len(board[0])-1)
