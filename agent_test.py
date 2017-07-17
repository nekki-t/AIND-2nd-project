"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import sample_players

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)


class MinMaxPlayerTest(unittest.TestCase):
    def setUp(self):
        self.player1 = game_agent.MinimaxPlayer(score_fn=self.custom_score, search_depth=3)
        self.player2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(self.player1, self.player2)

        minmax_value = self.player1.get_move(self.game, lambda: 10000)
        print(minmax_value)

    def custom_score(self, game, player):
        if game.is_loser(player):
            return float("-inf")
        if game.is_winner(player):
            return float("inf")
        remain_moves = len(game.get_legal_moves(player))
        opps_remain_moves = len(game.get_legal_moves(game.get_opponent(player)))

        return remain_moves / opps_remain_moves

class AlphaBetaPlayerTest(unittest.TestCase):
    def setUp(self):
        self.player1 = game_agent.AlphaBetaPlayer(score_fn=self.custom_score_2, search_depth=3)
        self.player2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(self.player1, self.player2)

        minmax_value = self.player1.get_move(self.game, lambda: 10000)

        test = self.player1.score(self.game, self)
        print(minmax_value)

    def custom_score(self, game, player):
        if game.is_loser(player):
            return float("-inf")
        if game.is_winner(player):
            return float("inf")
        remain_moves = len(game.get_legal_moves(player))
        opps_remain_moves = len(game.get_legal_moves(game.get_opponent(player)))

        # player.get_move(game, lambda: 10000)

        return remain_moves / opps_remain_moves
    def custom_score_2(self, game, player):

        remain_moves = len(game.get_legal_moves(player))
        return remain_moves * self.score_weight(game, player)

    def custom_score_3(self, game, player):

        remain_moves = len(game.get_legal_moves(player))
        opp_remain_moves = len(game.get_legal_moves(game.get_opponent(player)))
        my_score = remain_moves * self.score_weight(game, player)
        opp_score = opp_remain_moves * self.score_weight(game, game.get_opponent(player))
        return my_score - opp_score


    def score_weight(self, game, player):
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
        return score

if __name__ == '__main__':
    unittest.main()
