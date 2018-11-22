from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance



class PacmanAgent(Agent):
    def __init__(self, args, max_depth=3):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.path = None
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
        legals.remove(Directions.STOP)
        move = Directions.STOP
        # print("Capusles-> ",state.getCapsules())

        # action = self._get_action(state)

        # return action

        value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')


        for action in legals:
            temp = self.min_agent(state.generatePacmanSuccessor(action), 0, alpha, beta, 1)

            if temp > value:

                value = temp
                move = action

            alpha = max(alpha, value)

        return move

    def max_agent(self, state, depth, alpha, beta):
        if state.isWin() or state.isLose() or depth is self.max_depth:
            return state.getScore() + self.eval_function(state)

        value = float('-inf')
        for succ, _ in state.generatePacmanSuccessors():

            value = max(value, self.min_agent(succ, depth, alpha, beta, 1))
            if value >= beta:
                return value

            alpha = max(alpha, value)

        return value

    def min_agent(self, state, depth, alpha, beta, idxGhost):
        if state.isWin() or state.isLose() or depth is self.max_depth:
            return state.getScore() + self.eval_function(state)

        value = float('inf')

        for succ, _ in state.generateGhostSuccessors(idxGhost):
        # for action in legals:
        #     nextAction = state.generateSuccessor(1, action)
            value = min(value, self.max_agent(succ, depth + 1, alpha, beta))
            # value = min(value, self.max_agent(state.generatePacmanSuccessor(action), depth + 1, alpha, beta))
            # value = min(value, self.max_agent(nextAction, depth + 1, alpha, beta))

            if value <= alpha:
                return value

            beta = min(beta, value)

        return value

    def eval_function(self, state):

        actualFood = state.getFood()

        successorPos = state.getPacmanPosition()
        successorFood = state.getFood().asList()

        score = 0

        if actualFood[successorPos[0]][successorPos[1]]:
            score += 10
        newFoodDist = float('inf')
        for food in successorFood:
            foodDist = manhattanDistance(successorPos, food)

            newFoodDist = min([foodDist, newFoodDist])

        newGhostDist = float('inf')
        for ghost in state.getGhostPositions():

            ghostDist = manhattanDistance(successorPos, ghost)

            newGhostDist = min([newGhostDist, ghostDist])

        if newGhostDist < 2:  # to avoid be close to the Ghost
            score -= 500

        score = score + (1./newFoodDist)
        return score