from pacman_module.game import Agent
from pacman_module.pacman import Directions
from random import randint
from sys import setrecursionlimit


def getStateRepresentation(state):
    return (state.getPacmanPosition(),state.getGhostPositions()[0], state.getFood())

class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        setrecursionlimit(10000) # just to make it work in recursion

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

        print("")
        print("new eval")
        alpha = float('-inf')
        beta = float('inf')
        best_move = Directions.STOP
        v = float('-inf')
        print("first v", v)
        exploredStates.append(getStateRepresentation(state))
        print(state.generatePacmanSuccessors())

        for succ, move in state.generatePacmanSuccessors():
            print(move)
            exploredStates.append(getStateRepresentation(succ))
            new_v = self.min_value(succ, alpha, beta, exploredStates)
            print("Move : ", move, " value : ",new_v)
            if new_v >= v:
                v = new_v
                best_move = move
                print("new move :", move)
            if v >= beta:
                break
            alpha = max(alpha, v)
        return best_move

    def max_value(self, state, alpha, beta, exploredStates):
        if state.isWin() or state.isLose():
            return state.getScore()

        v = float('-inf')
        for succ, move in state.generatePacmanSuccessors():
            if getStateRepresentation(succ) not in exploredStates:
                exploredStates.append(getStateRepresentation(succ))
                v = max(v, self.min_value(succ, alpha, beta, exploredStates))
                if v >= beta: return v
                alpha = max(alpha, v)
        if v == float('-inf'): return float('inf')
        return v

    def min_value(self, state, alpha, beta, exploredStates):
        if state.isWin() or state.isLose():
            return state.getScore()

        v = float('inf')
        for succ, move in state.generateGhostSuccessors(1):
            if getStateRepresentation(succ) not in exploredStates:
                exploredStates.append(getStateRepresentation(succ))
                v = min(v, self.max_value(succ, alpha, beta, exploredStates))
                if v <= alpha: return v
                beta = min(beta, v)
        if v == float('inf'): return float('-inf')
        return v