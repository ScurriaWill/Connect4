import copy
import random
import Connect4Game as game_file


def return_move(b):
    board = copy.deepcopy(b)
    for col in range(7):
        if game_file.is_valid_location(board, col):
            row = game_file.get_next_open_row(board, col)
            game_file.drop_piece(board, row, col, 1)

            if game_file.winning_move(board, 1):
                game_over = True
    return random.randint(0, 6)
