"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    remain_moves = len(game.get_legal_moves(player))
    opp_remain_moves = len(game.get_legal_moves(game.get_opponent(player)))
    my_score = remain_moves * score_weight(game, player)
    opp_score = opp_remain_moves * score_weight(game, game.get_opponent(player))
    return my_score - opp_score

def score_weight(game, player):
    player_location = game.get_player_location(player)
    knight_moves = [(player_location[0] + 1, player_location[0] + 2)]
    knight_moves.append((player_location[0] + 1, player_location[0] - 2))
    knight_moves.append((player_location[0] - 1, player_location[0] + 2))
    knight_moves.append((player_location[0] - 1, player_location[0] - 2))
    knight_moves.append((player_location[0] + 2, player_location[0] + 1))
    knight_moves.append((player_location[0] + 2, player_location[0] - 1))
    knight_moves.append((player_location[0] - 2, player_location[0] + 1))
    knight_moves.append((player_location[0] - 2, player_location[0] - 1))

    score = 1
    player_legal_moves = game.get_legal_moves(player)
    for move in knight_moves:
        if move in player_legal_moves:
            score += 1
    return float(score)


class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, time_left):

        self.time_left = time_left

        no_legal_move = (-1, -1)
        best_move = no_legal_move
        remaining_moves = game.get_legal_moves()

        if len(remaining_moves) == 0:
            # no more moves
            return no_legal_move
        try:
            depth = 0
            while self.time_left() > self.TIMER_THRESHOLD:
                depth += 1
                best_move = self.alphabeta(game, depth)
        except SearchTimeout:
            return best_move

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        last_best_move = (-1, -1)
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout

        # TODO: finish this function!
        alphabeta = self.alphabeta_execute(game, depth, True)
        return alphabeta[1]

    def alphabeta_execute(self, game, depth, myturn, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        no_legal_move = (-1, -1)

        remaining_moves = game.get_legal_moves()

        if len(remaining_moves) == 0:
            # no more moves
            return game.utility(self), no_legal_move

        if depth == 0:
            return self.score(game, self), no_legal_move

        best_move = no_legal_move  # default

        # set default score for each turn
        if myturn:
            v = float("-inf")
        else:
            v = float("inf")

        turn = not myturn

        for m in remaining_moves:
            newmove = game.forecast_move(m)
            score, _ = self.alphabeta_execute(newmove, depth - 1, turn, alpha, beta)
            if myturn:
                if v < score:
                    v, best_move = score, m
                if v >= beta:
                    return v, best_move
                alpha = max(alpha, v)
            else:
                if v > score:
                    v, best_move = score, m
                if v <= alpha:
                    return v, best_move
                beta = min(beta, v)

        return v, best_move
