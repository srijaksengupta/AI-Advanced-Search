#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        self.wins = ["CC", "CB", "BC", "BB", "A"]
        self.fingprint = {
            "A": [(0, 8), (1, 3), (1, 7), (0, 1, 6), (0, 2, 4), (0, 2, 7), (0, 4, 5), (0, 1, 3, 4), (0, 1, 3, 5),
                  (0, 1, 3, 8), (0, 1, 7, 8), (0, 2, 6, 8), (1, 3, 5, 7), (0, 1, 4, 5, 6), (0, 1, 5, 6, 7),
                  (0, 1, 5, 6, 8), (0, 1, 3, 5, 7, 8)],
            "B": [(0, 2), (0, 4), (0, 5), (1, 4), (0, 1, 3), (1, 3, 5), (0, 1, 4, 5), (0, 1, 4, 6), (0, 1, 5, 6),
                  (0, 1, 6, 7), (0, 1, 6, 8), (0, 2, 4, 7), (0, 4, 5, 7), (0, 1, 3, 5, 8), (0, 1, 3, 5, 7)],
            "D": [(0, 1, 5), (0, 1, 7), (0, 1, 8)],
            "AB": [(0, 1, 4), (0, 2, 6), (1, 3, 4), (0, 1, 5, 7), (0, 1, 5, 8)],
            "AD": [(0, 1)]}

    def getAction(self, gameState, gameRules):
        # b gets the state and stores it
        b = ""
        y = 0
        while y < 3:
            b = b + self.estimate(gameState.boards[y])
            y = y + 1

        for action in gameState.getLegalActions(gameRules):
            s = gameState.generateSuccessor(action)
            # b gets the state and stores it
            b = ""
            i = 0
            while i < 3:
                b = b + self.estimate(s.boards[i])
                i = i + 1
            x = self.wins
            for i in x:
                if b == i:
                    best_action = action
                    break
                else:
                    continue
        return best_action
        # util.raiseNotDefined()

    def changeBoard(self, board, degree):
        nBoard = [False, False, False, False, False, False, False, False, False]
        if degree == 1:
            # 90 degrees rotation
            nBoard[0], nBoard[1], nBoard[2], nBoard[3] = board[6], board[3], board[0], board[7]
            nBoard[4], nBoard[5], nBoard[6], nBoard[7], nBoard[8] = board[4], board[1], board[8], board[5], board[2]
        if degree == 2:
            # 180 degrees rotation
            nBoard[0], nBoard[1], nBoard[2], nBoard[3] = board[8], board[7], board[6], board[5]
            nBoard[4], nBoard[5], nBoard[6], nBoard[7], nBoard[8] = board[4], board[3], board[2], board[1], board[0]
        if degree == 3:
            # 270 degrees rotation
            nBoard[0], nBoard[1], nBoard[2], nBoard[3] = board[2], board[5], board[8], board[1]
            nBoard[4], nBoard[5], nBoard[6], nBoard[7], nBoard[8] = board[4], board[7], board[0], board[3], board[6]
        if degree == 4:
            # Mirror rotation
            nBoard[0], nBoard[1], nBoard[2], nBoard[3] = board[2], board[1], board[0], board[5]
            nBoard[4], nBoard[5], nBoard[6], nBoard[7], nBoard[8] = board[4], board[3], board[8], board[7], board[6]
        return nBoard

    def estimate(self, board):
        positional_arr = dict()
        i = 0
        while i < 8:
            positional_arr[i] = []
            i = i + 1

        i = 0
        while i < 9:
            if board[i]:
                positional_arr[0].append(i)
            i = i + 1

        # This is where we rotate
        i = 0
        while i < 3:
            demo = self.changeBoard(board, i + 1)
            j = 0
            while j < 9:
                if demo[j]:
                    positional_arr[i + 1].append(j)
                j = j + 1
            i = i + 1

        # This is where we do mirror
        mBoard = self.changeBoard(board, 4)
        i = 0
        while i < 9:
            if mBoard[i]:
                positional_arr[4].append(i)
            i = i + 1

        i = 0
        while i < 3:
            demo = self.changeBoard(mBoard, i + 1)
            j = 0
            while j < 9:
                if demo[j]:
                    positional_arr[i + 5].append(j)
                j = j + 1
            i = i + 1

        i = 0
        while i < 8:
            if len(positional_arr[i]) == 0:
                return "C"
            myStates = tuple(positional_arr[i])
            states = self.fingprint["A"]
            if myStates in states:
                return "A"
            states = self.fingprint["B"]
            if myStates in states:
                return "B"
            if len(myStates) == 1 and positional_arr[i][0] == 4:
                return "CC"
            states = self.fingprint["D"]
            if myStates in states:
                return "D"
            states = self.fingprint["AB"]
            if myStates in states:
                return "AB"
            states = self.fingprint["AD"]
            if myStates in states:
                return "AD"
            i = i + 1
        return ""

class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
