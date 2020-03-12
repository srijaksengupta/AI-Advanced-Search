from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        flag = True
        # Here, we calculate the manhattan distance to the nearest food from the newPos
        distance_to_closestfood = - min(([manhattanDistance(newPos, x) for x in prevFood.asList()]))
        # Iterating through ghost states
        for s in newGhostStates:
            # Here, we handle situation where the current ghost position is the same as newPos
            # As stated above, we also need to deal with the situation where action = 'Stop'
            if s.getPosition() == newPos or action == 'Stop':
                flag = False
                break
        if flag is True:
            return distance_to_closestfood
        else:
            return -999999999

        # return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def min_val(state, depth, agentIndex):
            # Checking the terminal-test condition
            if self.terminaltest(state, depth):
                return self.evaluationFunction(state), 0
            v = 999999999
            # Check whether agent Index < number of agents - 1 to stay on same depth passed as argument of the function
            if agentIndex < state.getNumAgents() - 1:
                for action in state.getLegalActions(agentIndex):
                    # s stores successor game state after an agent takes a particular action
                    s = state.generateSuccessor(agentIndex, action)
                    movescore = min_val(s, depth, (agentIndex + 1) % state.getNumAgents())[0]
                    if movescore < v:
                        v, worst_action = movescore, action
                return v, worst_action
            # In this else condition, we move 1 depth backwards
            else:
                for action in state.getLegalActions(agentIndex):
                    # s stores successor game state after an agent takes a particular action
                    s = state.generateSuccessor(agentIndex, action)
                    movescore = max_val(s, depth - 1, 0)[0]
                    if movescore < v:
                        v, worst_action = movescore, action
                return v, worst_action


        def max_val(state, depth, agentIndex):
            # Checking the terminal-test condition
            if self.terminaltest(state, depth):
                return self.evaluationFunction(state), 0
            v = -999999999
            for action in state.getLegalActions(agentIndex):
                # s stores successor game state after an agent takes a particular action
                s = state.generateSuccessor(agentIndex, action)
                movescore = min_val(s, depth, (agentIndex + 1) % state.getNumAgents())[0]
                if movescore > v:
                    v, best_action = movescore, action
            return v, best_action

        agentIndex = 0
        # Here, we return the minimax actions
        return max_val(gameState, self.depth - 1, agentIndex)[1]
        # util.raiseNotDefined()

    # This function checks whether the given state is a terminal state or not and returns corresponding boolean value
    def terminaltest(self, state, depth):
        if state.isWin() or state.isLose() or depth < 0:
            return True
        else:
            return False

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def min_val(state, depth, agentIndex, a, b):
            # Checking the terminal-test condition
            if self.terminaltest(state, depth):
                return self.evaluationFunction(state), 0
            v = 999999999
            # Check whether agent Index < number of agents - 1 to stay on same depth passed as argument of the function
            if agentIndex < state.getNumAgents() - 1:
                for action in state.getLegalActions(agentIndex):
                    # s stores successor game state after an agent takes a particular action
                    s = state.generateSuccessor(agentIndex, action)
                    movescore = min_val(s, depth, (agentIndex + 1) % state.getNumAgents(), a, b)[0]
                    if movescore < v:
                        v, worst_action = movescore, action
                    if v < a:
                        return (v, worst_action)
                    b = min(b, v)
                return v, worst_action
            # In this else condition, we move 1 depth backwards
            else:
                for action in state.getLegalActions(agentIndex):
                    # s stores successor game state after an agent takes a particular action
                    s = state.generateSuccessor(agentIndex, action)
                    movescore = max_val(s, depth - 1, 0, a, b)[0]
                    if movescore < v:
                        v, worst_action = movescore, action
                    if v < a:
                        return (v, worst_action)
                    b = min(b, v)
                return v, worst_action

        def max_val(state, depth, agentIndex, a, b):
            # Checking the terminal-test condition
            if self.terminaltest(state, depth):
                return self.evaluationFunction(state), 0
            v = -999999999
            for action in state.getLegalActions(agentIndex):
                # s stores successor game state after an agent takes a particular action
                s = state.generateSuccessor(agentIndex, action)
                movescore = min_val(s, depth, (agentIndex + 1) % state.getNumAgents(), a, b)[0]
                if movescore > v:
                    v, best_action = movescore, action
                if v > b:
                    return v, best_action
                a = max(a, v)
            return v, best_action

        agentIndex = 0
        # Here, we return the minimax actions
        return max_val(gameState, self.depth - 1, agentIndex, -999999999, 999999999)[1]
        # util.raiseNotDefined()

    # This function checks whether the given state is a terminal state or not and returns corresponding boolean value
    def terminaltest(self, state, depth):
        if state.isWin() or state.isLose() or depth < 0:
            return True
        else:
            return False
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        agentIndex = 0
        # Here, we return the expectimax actions
        return self.expectimax(gameState, self.depth, agentIndex)[1]

    # This function checks whether the given state is a terminal state or not and returns corresponding boolean value
    def terminaltest(self, state, depth):
        if state.isWin() or state.isLose() or depth == 0:
            return True
        else:
            return False
    def alt_vassign(self, state, agentIndex, expectscore, v):
        prob = 1.0 / len(state.getLegalActions(agentIndex))
        v += prob * expectscore * 100
        return v

    def expectimax(self, gameState, depth, agentIndex):
        # Checking the terminal-test condition
        state = gameState
        if self.terminaltest(state, depth):
            return self.evaluationFunction(state), 0

        # Here, we assign v to 0 initially
        # If the agentIndex is 0, then we assign a very low value to v to mimic infinity
        v = 0
        if agentIndex == 0:
            v = -99999999
        if agentIndex < state.getNumAgents() - 1:
            for action in state.getLegalActions(agentIndex):
                # s stores successor game state after an agent takes a particular action
                s = state.generateSuccessor(agentIndex, action)
                expectscore = self.expectimax(s, depth, (agentIndex + 1) % state.getNumAgents())[0]
                if agentIndex == 0:
                    if expectscore > v:
                        v, best_action = expectscore, action
                else:
                    v, best_action = self.alt_vassign(state, agentIndex, expectscore, v), action
            return v, best_action
        else:
            for action in state.getLegalActions(agentIndex):
                # s stores successor game state after an agent takes a particular action
                s = state.generateSuccessor(agentIndex, action)
                expectscore = self.expectimax(s, depth - 1, (agentIndex + 1) % state.getNumAgents())[0]
                if agentIndex == 0:
                    if expectscore > v:
                        v, best_action = expectscore, action
                else:
                    v, best_action = self.alt_vassign(state, agentIndex, expectscore, v), action
            return v, best_action



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    state = currentGameState

    # Similar to Reflex Agent, we can retrieve the following information
    # The first 2 are the present position of Pacman and the food in the current game state
    presPos = state.getPacmanPosition()
    presFood = state.getFood()

    # The next 2 are the Ghost positions and Ghost states in the current game state respectively
    presGhostPos = state.getGhostPositions()
    presGhostStates = state.getGhostStates()

    # Here, we get the position of the power pellets in the current game state
    presPower = state.getCapsules()

    # scaredTimes holds the number of moves that each ghost will remain scared in the current game state.
    # This is caused because of Pacman eating a power pellet
    scaredTimes = [ghostState.scaredTimer for ghostState in presGhostStates]

    # flag variable is a boolean variable to consider whether the ghost is scared or not
    flag = False
    if max(scaredTimes) == 0:
        flag = False
    else:
        flag = True

    # Here, we find the manhattan distance to the closest food
    distance_to_closestfood = min([presFood.width + presFood.height] + [manhattanDistance(presPos, x)
                                                                         for x in presFood.asList()])
    # For scoring, we try a method as seen in the lecture slides
    foodpoints = 1
    if len(presFood.asList()) != 0:
        foodpoints = 1 / distance_to_closestfood
    tot_foodpoints = foodpoints * 1

    # Here, we find the manhattan distance to the closest power pellet
    distance_to_closestpowerpellet = min([len(presPower)] + [manhattanDistance(presPos, x) for x in presPower])
    # For scoring, we try a method as seen in the lecture slides
    powerpelletpoints = 1
    if len(presPower) != 0:
        powerpelletpoints = 1 / distance_to_closestpowerpellet
    tot_powerpelletpoints = powerpelletpoints * 3

    # Here, we find the manhattan distance to the closest ghost
    distance_to_closestghost = min([manhattanDistance(presPos, x) for x in presGhostPos])
    # For scoring, we try a method as seen in the lecture slides
    # Negative in this case because it is not desired
    ghostpoints = -100
    if distance_to_closestghost >= 1:
        ghostpoints = 1 / distance_to_closestghost
    tot_ghostpoints = 0
    if flag:
        # Ghost constant to multiply with ghostpoints is 100 if scared state is active which is checked by flag value
        tot_ghostpoints = ghostpoints * 100
    else:
        tot_ghostpoints = ghostpoints * 1

    tot_score = state.getScore() + tot_foodpoints + tot_powerpelletpoints + tot_ghostpoints
    return tot_score

# Abbreviation
better = betterEvaluationFunction

