from pacman_module.game import Agent
from pacman_module.pacman import Directions
from random import randint
from sys import setrecursionlimit


def getStateRepresentation(state):
    return (state.getPacmanPosition(), state.getGhostPositions()[0], state.getFood())


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        setrecursionlimit(10000)  # just to make it work in recursion

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
        exploredStates = []
        legals = state.getLegalActions()

        best_move = Directions.STOP
        print("new eval")
        best_score = self.min_agent(state.generatePacmanSuccessor(best_move), exploredStates)
        print("ghost ", state.getGhostPositions()[0])
        exploredStates.append(getStateRepresentation(state))
        for succ, move in state.generatePacmanSuccessors():
            exploredStates.append(getStateRepresentation(succ))
            minimax_score = self.min_agent(succ, exploredStates)
            if minimax_score >= best_score:
                print("ok")
                best_score = minimax_score
                best_move = move
                print(move)
        print("Best score", best_score)
        return best_move

    def max_agent(self, state, exploredStates):
        if state.isWin() or state.isLose():
            return state.getScore()

        min_scores = [float('-inf')]
        for succ, move in state.generatePacmanSuccessors():
            if getStateRepresentation(succ) not in exploredStates:
                exploredStates.append(getStateRepresentation(succ))
                min_scores.append(self.min_agent(succ, exploredStates))
        print(min_scores)
        return max(min_scores)

    def min_agent(self, state, exploredStates):
        if state.isWin() or state.isLose():
            return state.getScore()

        max_scores = [float('inf')]
        for succ, move in state.generateGhostSuccessors(1):
            if getStateRepresentation(succ) not in exploredStates:
                exploredStates.append(getStateRepresentation(succ))
                max_scores.append(self.max_agent(succ, exploredStates))
        return min(max_scores)
