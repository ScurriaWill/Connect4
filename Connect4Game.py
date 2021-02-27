import numpy as np
import pygame
import sys
import math
import random

from GriffinAI import GriffinAI
from WillAI import WillAI

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

usingAI = False


def create_board():
    b = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return b


def drop_piece(b, r, c, piece):
    b[r][c] = piece


def is_valid_location(b, c):
    return b[ROW_COUNT - 1][c] == 0


def get_next_open_row(b, c):
    for r in range(ROW_COUNT):
        if b[r][c] == 0:
            return r


def print_board(b):
    print(np.flip(b, 0))


def winning_move(b, piece):
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
will_ai = WillAI()
griffin_ai = GriffinAI()
ai_turn_time = 2000  # in ms

pygame.init()

SQUARE_SIZE = 100

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)

RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 75)

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
            col = will_ai.make_move(board)
            if pygame.time.get_ticks() < end_time:
                pygame.time.wait(end_time - pygame.time.get_ticks())

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    label = myFont.render("Will's AI wins!!", True, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

            else:
                turn -= 1

        # Ask for Player 2 Input
        else:
            start_time = pygame.time.get_ticks()
            end_time = start_time + ai_turn_time
            col = griffin_ai.make_move(board)
            if pygame.time.get_ticks() < end_time:
                pygame.time.wait(end_time - pygame.time.get_ticks())


            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    label = myFont.render("Griffin's AI wins!!", True, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

            else:
                turn -= 1

        draw_board(board)

        turn += 1
        turn = turn % 2

        if game_over:
            pygame.time.wait(3000)
