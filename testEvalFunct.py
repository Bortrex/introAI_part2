from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue, manhattanDistance
from kruskal import Graph
import numpy as np


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.path = None

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
        legals.remove(Directions.STOP)

        # print("Capusles-> ",state.getCapsules())

        # action = self._get_action(state)

        scores = [self.eval_function(state, successor) for successor, _ in state.generatePacmanSuccessors()]
        bestScores = max(scores)
        # it just returns the index of the best legal move =) according to the bestScores ;)
        bestIdx = [idx for idx in range(len(scores)) if scores[idx] is bestScores]

        chosenIdx = np.random.choice(bestIdx)
        # print(bestIdx, chosenIdx)
        return legals[chosenIdx]
        # return action

    def eval_function(self, state, successor):

        actualFood = state.getFood()

        walls = state.getWalls()

        # To add to the score a diagonal value of the height and width
        # if Pacman and ghost or food are farthest in the game.
        maxLength = walls.height - 2 + walls.width - 2

        successorPos = successor.getPacmanPosition()
        successorFood = successor.getFood().asList()

        score = 0

        if actualFood[successorPos[0]][successorPos[1]]:
            score += 10

        newFoodDist = np.inf

        for food in successorFood:
            foodDist = manhattanDistance(successorPos, food)

            newFoodDist = min([foodDist, newFoodDist])

        newGhostDist = np.inf

        for ghost in successor.getGhostPositions():

            ghostDist = manhattanDistance(successorPos, ghost)

            newGhostDist = min([newGhostDist, ghostDist])

        if newGhostDist < 2:  # to avoid be close to the Ghost
            score -= 500

        score = score + (1. / newFoodDist) + (newGhostDist / maxLength)

        return score
