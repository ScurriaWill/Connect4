import numpy as np
import pygame
import sys
import math
import random

import GriffinAI
import WillAI

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6  # normally 6
COLUMN_COUNT = 7  # normally 7
cont_spaces_to_win = 4

usingAI = True
ai_max_time = 10000


def create_board():
    b = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return b


def drop_piece(b, r, c, piece):
    b[r][c] = piece


def is_valid_location(b, c):
    if c >= COLUMN_COUNT or c < 0:
        return False
    return b[ROW_COUNT - 1][c] == 0


def get_next_open_row(b, c):
    for r in range(ROW_COUNT):
        if b[r][c] == 0:
            return r


def print_board(b):
    print(np.flip(b, 0))


def winning_move(b, piece):
    # TODO: make method handle games with longer sequences to win
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if b[r][c] == piece and b[r][c + 1] == piece and b[r][c + 2] == piece and b[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if b[r][c] == piece and b[r + 1][c] == piece and b[r + 2][c] == piece and b[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if b[r][c] == piece and b[r + 1][c + 1] == piece and b[r + 2][c + 2] == piece and b[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if b[r][c] == piece and b[r - 1][c + 1] == piece and b[r - 2][c + 2] == piece and b[r - 3][c + 3] == piece:
                return True


def draw_board(b):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if b[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif b[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
game_over = False
turn = random.randint(0, 1)
ai_turn_time = 750  # in ms
ai_1_owner = "Will"
ai_2_owner = "Griffin"

pygame.init()

scalar = 1
SQUARE_SIZE = int(100 * scalar)  # normally 100

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
num_moves = 0

size = (width, height)

RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", int(60 * scalar))

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif not usingAI:

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                posX = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posX, int(SQUARE_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posX, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                # Ask for Player 1 Input
                if turn == 0:
                    posX = event.pos[0]
                    col = int(math.floor(posX / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        num_moves += 1

                        if winning_move(board, 1):
                            label = myFont.render("Player 1 wins!!", True, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                    else:
                        turn -= 1

                # Ask for Player 2 Input
                else:
                    posX = event.pos[0]
                    col = int(math.floor(posX / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        num_moves += 1

                        if winning_move(board, 2):
                            label = myFont.render("Player 2 wins!!", True, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                    else:
                        turn -= 1

                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)

    if usingAI:

        if turn == 0:
            start_time = pygame.time.get_ticks()
            end_time = start_time + ai_turn_time
            col = WillAI.return_move(board, cont_spaces_to_win, num_moves)
            if pygame.time.get_ticks() < end_time:
                pygame.time.wait(end_time - pygame.time.get_ticks())

            if pygame.time.get_ticks() > start_time + ai_max_time:
                col = random.randint(0, 6)
                print(ai_1_owner + "'s AI took too long and got penalized with a random move")

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)
                num_moves += 1

                if winning_move(board, 1):
                    label = myFont.render(ai_1_owner + "'s AI wins!!", True, RED, BLACK)
                    screen.blit(label, (40, 10))
                    game_over = True

            else:
                turn -= 1

        # Ask for Player 2 Input
        else:
            start_time = pygame.time.get_ticks()
            end_time = start_time + ai_turn_time
            col = GriffinAI.get_move(board, 2)
            if pygame.time.get_ticks() < end_time:
                pygame.time.wait(end_time - pygame.time.get_ticks())

            if pygame.time.get_ticks() > start_time + ai_max_time:
                col = random.randint(0, 6)
                print(ai_2_owner + "'s AI took too long and got penalized with a random move")

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                num_moves += 1

                if winning_move(board, 2):
                    label = myFont.render(ai_2_owner + "'s AI wins!!", True, YELLOW, BLACK)
                    screen.blit(label, (40, 10))
                    game_over = True

            else:
                turn -= 1

        draw_board(board)

        turn += 1
        turn = turn % 2

        if game_over:
            pygame.time.wait(3000)
