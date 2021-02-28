import copy
import sys


class WillAI:

    @staticmethod
    def make_move(board):
        """Search game state to determine best action; use alpha-beta pruning. """
        # state = copy.deepcopy(board)
        state = board
        turn = -1
        d = 7

        # Functions used by alpha beta
        def max_value(b, alpha, bet, depth):
            if cutoff_search(b, depth):
                return b.calculate_heuristic()

            var = -sys.maxsize
            for c in b.generate_children(turn):
                if c in seen:
                    continue
                var = max(var, min_value(c, alpha, bet, depth + 1))
                seen[c] = alpha
                if var >= bet:
                    # Min is going to completely ignore this route
                    # since v will not get any lower than beta
                    return var
                alpha = max(alpha, var)
            if var == -sys.maxsize:
                # If win/loss/draw not found, don't return -infinity to MIN node
                return sys.maxsize
            return var

        def min_value(pos, alpha, b, depth):
            if cutoff_search(pos, depth):
                return pos.calculate_heuristic()

            var = sys.maxsize
            for c in pos.generate_children(turn):
                if c in seen:
                    continue
                var = min(var, max_value(c, alpha, b, depth + 1))
                seen[c] = alpha
                if var <= alpha:
                    # Max is going to completely ignore this route
                    # since v will not get any higher than alpha
                    return var
                b = min(b, var)
            if var == sys.maxsize:
                # If win/loss/draw not found, don't return infinity to MAX node
                return -sys.maxsize
            return var

        # Keep track of seen states using their hash
        seen = {}

        # Body of alpha beta_search:
        cutoff_search = (lambda pos, depth: depth > d or pos.terminal_node_test())
        best_score = -sys.maxsize
        beta = sys.maxsize
        best_action = None
        for child in state.generate_children(turn):
            v = min_value(child, best_score, beta, 1)
            if v > best_score:
                best_score = v
                best_action = child
        return best_action

    @staticmethod
    def will_ai():
        """WillAI"""
