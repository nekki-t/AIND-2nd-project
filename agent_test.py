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
        self.player1 = game_agent.AlphaBetaPlayer(score_fn=self.custom_score, search_depth=3)
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


if __name__ == '__main__':
    unittest.main()
