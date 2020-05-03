# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import math
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        print("LEgalMoves", legalMoves)
        print("Scores", scores)
        print("BestIndices", bestIndices)
        print("ChoosenIndex", chosenIndex)
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
#        print("newPos", newPos)
#        print("newFood", newFood.asList())
#        print("newGhostStates", newGhostStates)
#        print("newScaredTimes", newScaredTimes)
        
        
        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        
        # rate closer food higher
        foodDistances = [manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]
        score -= min(foodDistances, default=0)
        
        # keep distance to ghosts

        ghostDistances = [ manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates ]
        if min(ghostDistances, default=2) <= 1:
            score = 0
        
        return score

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
        
        def min_max(gameState, depth, agentIndex):
#            print("Current Agent", agentIndex)
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:
                return max(min_max(gameState.generateSuccessor(agentIndex, nextState), depth, 1) for nextState in gameState.getLegalActions(agentIndex))
            else:
                nextAgent = (agentIndex + 1) % (gameState.getNumAgents())
                if nextAgent == 0:
                    depth += 1
#                print("Next Agent Index", nextAgent)
#                print("Num Agents", state.getNumAgents())
                return min(min_max(gameState.generateSuccessor(agentIndex, newState), depth,  nextAgent) for newState in gameState.getLegalActions(agentIndex))
                
        #choose the best option
        best_path_value = -math.inf
        best_action = Directions.WEST
        
        for action in gameState.getLegalActions(0):
            path_value = min_max(gameState.generateSuccessor(0, action), 0, 1)
            if path_value > best_path_value or best_path_value == -math.inf:
                best_path_value = path_value
                best_action = action
        
        return best_action
        
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(agent, depth, gameState, alpha, beta):
            value = -math.inf
            for action in gameState.getLegalActions(0):
                value = max(value, dispatch(1, depth, gameState.generateSuccessor(agent, action), alpha, beta))
                if value > beta: #value is bigger than mins best option --> this path never gets choosen --> stop calculating other leaves
                    return value
                alpha = max(alpha, value)
            return value
        
        def min_value(agent, depth, gameState, alpha, beta):
            value = math.inf
            nextAgent = (agent + 1) % gameState.getNumAgents()
            if nextAgent == 0:
                depth += 1
            
            for action in gameState.getLegalActions(agent):
                value = min(value, dispatch(nextAgent, depth, gameState.generateSuccessor(agent, action), alpha, beta))
                if value < alpha:
                    return value
                beta = min(beta, value)
            return value
            
        def dispatch(agent, depth, gameState, alpha, beta):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agent == 0:
                return max_value(agent, depth, gameState, alpha, beta)
            else:
                return min_value(agent, depth, gameState, alpha, beta)
            
        #choose the best option
        best_path_value = -math.inf
        best_action = Directions.WEST
        alpha = -math.inf
        beta = math.inf
        for action in gameState.getLegalActions(0):
            path_value = dispatch(1, 0, gameState.generateSuccessor(0, action), alpha, beta)
            if path_value > best_path_value or best_path_value == -math.inf:
                best_path_value = path_value
                best_action = action
            if best_path_value > beta:
                return best_path_value
            alpha = max(alpha, best_path_value)
        return best_action

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
        def max_value(agent, depth, gameState):
            value = -math.inf
            for action in gameState.getLegalActions(0):
                value = max(value, dispatch(1, depth, gameState.generateSuccessor(agent, action)))
            return value
        
        def expected_value(agent, depth, gameState):
            value = 0
            nextAgent = (agent + 1) % gameState.getNumAgents()
            if nextAgent == 0:
                depth += 1
            probability = 1 / float(len(gameState.getLegalActions(agent)))
            for action in gameState.getLegalActions(agent):
                value += probability * dispatch(nextAgent, depth, gameState.generateSuccessor(agent, action))
            return value
            
        def dispatch(agent, depth, gameState):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agent == 0:
                return max_value(agent, depth, gameState)
            else:
                return expected_value(agent, depth, gameState)
            
        #choose the best option
        best_path_value = -math.inf
        best_action = Directions.WEST
        for action in gameState.getLegalActions(0):
            path_value = dispatch(1, 0, gameState.generateSuccessor(0, action))
            if path_value > best_path_value or best_path_value == -math.inf:
                best_path_value = path_value
                best_action = action
        return best_action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
        
    # rate closer food higher
    foodlist = food.asList()
    foodDistances = [manhattanDistance(pos, foodPos) for foodPos in foodlist]
#    score -= min(foodDistances, default=0)
    if len(foodDistances) != 0:
        score -= sum(foodDistances) / len(foodDistances)
    
    # rewarding food pellets
    if pos in foodlist:
        print("reward")
        score += 10
    
    # keep distance to ghosts

    ghostDistances = [ manhattanDistance(pos, ghostState.getPosition()) for ghostState in ghostStates ]
    if min(ghostDistances, default=2) <= 1:
        score = 0
    
    return score

# Abbreviation
better = betterEvaluationFunction
