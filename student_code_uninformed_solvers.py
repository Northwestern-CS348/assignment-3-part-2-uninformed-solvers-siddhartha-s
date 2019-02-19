
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)


    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # Student code goes here

        if self.currentState not in self.visited:
            # Enters here if it's visiting the state for the first time
            self.visited[self.currentState] = True
            return self.currentState.state == self.victoryCondition

        if self.currentState.state == self.victoryCondition:
            # If the state we're already at is the victoryCondition
            return True

        if not self.currentState.children:
            # Enters here if the current state has been visited for the first time and children haven't been generated
            # and linked
            movables = self.gm.getMovables()

            # The whole if branch and for `move` loop and for `child` loop below is to populate
            # and link parent and children
            if movables:
                for move in movables:
                    self.gm.makeMove(move)
                    newState = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
                    newState.parent = self.currentState
                    self.currentState.children.append(newState)
                    self.gm.reverseMove(move)

        made_a_move = False

        children_list_length = len(self.currentState.children)

        # The for loop below checks whether there are any unvisited children and if there are, visits the first one.
        for x in range(self.currentState.nextChildToVisit, children_list_length):
            if self.currentState.children[x] not in self.visited:
                self.currentState.nextChildToVisit = x
                self.gm.makeMove(self.currentState.children[x].requiredMovable)
                self.currentState = self.currentState.children[x]
                self.visited[self.currentState] = True
                made_a_move = True
                break

        # If the above loop visits a child, we check whether the child is the victory condition
        if made_a_move and self.currentState.state == self.victoryCondition:
            # we have visited a child and it's the victory condition
            return True
        elif made_a_move and self.currentState.state != self.victoryCondition:
            # we have visited a child and it isn't the victory condition.
            return False
        else:
            # If we reach here, there are no children left to visit. So we back-track.
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            self.solveOneStep()

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        # Student code goes here

        # if self.currentState.state == self.victoryCondition:
        #     return True
        # else:
        #     if not self.currentState.children:
        #         movables = self.gm.getMovables()
        #         for move in movables:
        #             gs = self.gm.makeMove(move).getGameState()
        #             self.currentState.children.append(gs)
        #             BFSQueue.append(gs)
        #
        #
