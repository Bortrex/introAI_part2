from pacman_module.game import Agent
from pacman_module.pacman import Directions
from random import randint
import numpy as np

class PacmanAgent(Agent):
    def __init__(self, args, max_depth=3):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.max_depth = max_depth

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        legals = state.getLegalActions()

        best_move = Directions.STOP
        best_score = self.min_agent(state.generatePacmanSuccessor(best_move), 0)

        for succ, move in state.generatePacmanSuccessors():
            minimax_score = self.min_agent(succ, 0)
            if minimax_score >= best_score:
                best_score = minimax_score
                best_move = move

        print("Best score", best_score)
        return best_move

    def max_agent(self, state, depth):
        if state.isWin() or state.isLose():
            return state.getScore()
        return max([self.min_agent(succ, depth) for (succ, move) in state.generatePacmanSuccessors()])

    def min_agent(self, state, depth):
        if state.isWin() or state.isLose() or depth is self.max_depth:
            return state.getScore()
        return min([self.max_agent(succ, depth + 1) for (succ, move) in state.generateGhostSuccessors(1)])
