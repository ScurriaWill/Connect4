import random


def return_move(board):
    return random.randint(0, len(board[0])-1)
