from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue
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
        # legals = state.getLegalActions()
        # legals.remove(Directions.STOP)
        print(state.getGhostPositions())
        self.get_max(state, 0)
        print("Capusles-> ",state.getCapsules())

        action = self._get_action(state)
        return action

    def get_max(self, state, depth):
        if depth is state.isWin() or state.isLose():
            return self.eval_function(state)

        value = -np.inf
        legals = state.getLegalActions()

        for action in legals:
            value = max(value, self.get_min(state.generatePacmanSuccessors(), depth, 1))

        return value

    def get_min(self, state, depth, agent_idx):
        pass

    def eval_function(self, state):
        pass

    def _get_action(self, state):
        """
        Auxiliary function of get_action
        """

        # If the path is not computed yet, we compute it
        if self.path is None:
            self.path = self.astar(state, self.kruskal)

        # Pops the next move of the path
        move = self.path[0]
        self.path.pop(0)

        return move

    def astar(self, start, heuristic):
        """
        Computes a winning path according to A* search algo

        Arguments:
        ----------
        - `start`: the initial game state
        - `heuristic`: a heuristic function

        Return:
        - the winning path computed by A* algorithm
        """
        explored = []
        fringe = PriorityQueue()
        fringe.push((start, []), 0)

        while True:
            node = fringe.pop()
            cost, state, path = node[0], node[1][0], node[1][1]
            pacmanState = (state.getPacmanPosition(), state.getFood())

            if pacmanState not in explored:
                explored.append(pacmanState)
                for successor, move in state.generatePacmanSuccessors():
                    # Testing if goal state:
                    goalState = True
                    for i in successor.getFood():
                        for j in i:
                            if j:  # not goal state, keep expanding
                                goalState = False
                    if goalState:
                        return path + [move]
                    else:
                        goals = successor.getFood().asList()
                        additionalCost = 0.001 if successor.getPacmanPosition() in state.getFood().asList() else 1
                        fringe.push((successor, path + [move]),
                                    len(path) + additionalCost
                                    + heuristic(successor.getPacmanPosition(),
                                                goals))

    def manhattan(self, position, goals):
        """
        Computes the Manhattan distance between 'position' and the farthest goal

        Arguments:
        ----------
        - `position`: the position (of Pacman)
        - `goals`: a list of positions corresponding to the goals (food dots)

        Return:
        -------
        - Manhattan distance between position and the farthest goal
        """
        distances = []
        for goal in goals:
            distances.append(abs(position[0] - goal[0])
                             + abs(position[1] - goal[1]))
        return max(distances)

    def kruskal(self, position, goals):
        """
        Computes the Manhattan distance between 'position' and the farthest goal

        Arguments:
        ----------
        - `position`: the position (of Pacman)
        - `goals`: a list of positions corresponding to the goals (food dots)

        Return:
        -------
        - Manhattan distance between position and the farthest goal
        """
        vertices = [position] + goals
        g = Graph(len(vertices))
        for i in range(len(vertices)):
            for j in range(i, len(vertices)):
                g.addEdge(i, j, abs(vertices[i][0] - vertices[j][0]) + abs(vertices[i][1] - vertices[j][1]))
        result = g.KruskalMST()
        sum = 0
        for u, v, weight in result:
            sum = sum + weight
        return sum
