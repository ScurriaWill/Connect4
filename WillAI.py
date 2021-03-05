import copy
import sys

DEPTH = 7
WILL_AI_PIECE = 1
OPP_PIECE = 2
WINDOW_LENGTH = 4
ROW_COUNT = 6
COLUMN_COUNT = 7
EMPTY = 0


def return_move(b, num_win, num_moves):
    global ROW_COUNT, COLUMN_COUNT, WINDOW_LENGTH, WILL_AI_PIECE, OPP_PIECE, EMPTY
    ROW_COUNT = len(b)
    COLUMN_COUNT = len(b[0])
    WINDOW_LENGTH = num_win
    WILL_AI_PIECE = 1
    OPP_PIECE = 2
    EMPTY = 0
    board = copy.deepcopy(b)
    col, minimax_score = minimax(board, DEPTH, -sys.maxsize, sys.maxsize, True)
    # col, negamax_score = negamax(board, DEPTH, -sys.maxsize, sys.maxsize, True, num_moves)
    return col


def negamax(board, depth, alpha, beta, is_will_ai, num_moves):
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, WILL_AI_PIECE if is_will_ai else OPP_PIECE):
                return None, sys.maxsize if is_will_ai else -sys.maxsize
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, score_position(board, WILL_AI_PIECE)

    temp = (COLUMN_COUNT * ROW_COUNT - 1 - num_moves) // 2
    if beta > temp:
        beta = temp
        if alpha >= beta:
            return beta

    valid_locations = get_valid_locations(board)
    column = valid_locations[0]
    for col in valid_locations:
        row = get_next_open_row(board, col)
        b_copy = board.copy()
        moves_copy = num_moves
        drop_piece(b_copy, row, col, WILL_AI_PIECE if is_will_ai else OPP_PIECE)
        moves_copy += 1
        new_score = -negamax(b_copy, depth - 1, -alpha, -beta, not is_will_ai, moves_copy)[1]

        if new_score >= beta:
            return col, new_score
        if new_score > alpha:
            alpha = new_score
            column = col

    return column, alpha


def minimax(board, depth, alpha, beta, maximizing_player):
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, WILL_AI_PIECE):
                return None, sys.maxsize
            elif winning_move(board, OPP_PIECE):
                return None, -sys.maxsize
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, score_position(board, WILL_AI_PIECE)
    valid_locations = get_valid_locations(board)
    if maximizing_player:
        value = -sys.maxsize
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, WILL_AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = sys.maxsize
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, OPP_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def evaluate_window(window, piece):
    score = 0
    opp_piece = OPP_PIECE
    if piece == OPP_PIECE:
        opp_piece = WILL_AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece \
                    and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece \
                    and board[r-3][c+3] == piece:
                return True


def is_valid_location(board, col):
    if 0 > col or col > COLUMN_COUNT - 1:
        return False
    return board[ROW_COUNT-1][col] == 0


def get_valid_locations(board):
    valid_locations = []
    for i in range(COLUMN_COUNT):
        col = int(COLUMN_COUNT // 2 + (1 - 2 * (i % 2)) * (i + 1) / 2)
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def is_terminal_node(board):
    return winning_move(board, WILL_AI_PIECE) or winning_move(board, OPP_PIECE) or len(get_valid_locations(board)) == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def drop_piece(board, row, col, piece):
    board[row][col] = piece
