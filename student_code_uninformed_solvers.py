
from solver import *
from collections import deque



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
                    new_gstuple = self.gm.getGameState()

                    # checks whether the move will return the state to the parent state.
                    if self.currentState.parent and new_gstuple == self.currentState.parent.state:
                        self.gm.reverseMove(move)
                        continue
                    else:
                        newState = GameState(new_gstuple, self.currentState.depth+1, move)
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
        self.bfsQ = deque()
        self.bfsQ.append(self.currentState)
        self.front = 0

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

        if self.currentState not in self.visited:
            # Enters here if it's visiting the state for the first time
            self.visited[self.currentState] = True
            return self.currentState.state == self.victoryCondition

        if self.currentState.state == self.victoryCondition:
            # If the state we're already at is the victoryCondition
            return True

        # The whole if branch and for `move` loop and for `child` loop below is to populate
        # and link parent and children and populate the queue

        if not self.currentState.children:
            movables = self.gm.getMovables()

            if movables:
                for move in movables:
                    self.gm.makeMove(move)
                    new_gstuple = self.gm.getGameState()

                    # checks whether the move will return the state to the parent state.
                    # if self.currentState.parent and new_gstuple == self.currentState.parent.state:
                    #     self.gm.reverseMove(move)
                    #     continue
                    # else:
                    newState = GameState(new_gstuple, self.currentState.depth+1, move)
                    newState.parent = self.currentState
                    self.currentState.children.append(newState)
                    self.bfsQ.append(newState)
                    self.gm.reverseMove(move)

        while True:
            self.front += 1
            if self.bfsQ[self.front] not in self.visited:
                break

        how_to_reach = list()

        #The next state we have to reach is in the front of bfsQ
        state_to_reach = self.bfsQ[self.front]

        while self.currentState.parent:
            #move the game master to the root of the tree
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        while state_to_reach.parent:
            #building path to state_to_reach
            how_to_reach.append(state_to_reach.requiredMovable)
            state_to_reach = state_to_reach.parent

        #syncing both gamemaster and currentState to state_to_reach
        while len(how_to_reach) > 0:
            move = how_to_reach.pop()
            self.gm.makeMove(move)
            movedown_tuple = self.gm.getGameState()
            for x in self.currentState.children:
                if x.state == movedown_tuple:
                    self.currentState = x
                    self.visited[x] = True
                    break

        self.visited[self.currentState] = True

        if self.currentState.state == self.victoryCondition:
            return True
        else:
            return False
