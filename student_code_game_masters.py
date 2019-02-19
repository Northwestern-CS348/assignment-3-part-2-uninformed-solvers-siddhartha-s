from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        #peg1: Checking what's on peg1
        on_peg1 = parse_input("fact: (on ?x peg1)")
        whats_on_peg1 = self.kb.kb_ask(on_peg1)

        disks_on_peg1 = []

        if whats_on_peg1:
            for x in whats_on_peg1:
                disks_on_peg1.append(int(x.bindings_dict['?x'].replace('disk', '')))

        disks_on_peg1.sort()

        # peg2: Checking what's on peg1
        on_peg2 = parse_input("fact: (on ?x peg2)")
        whats_on_peg2 = self.kb.kb_ask(on_peg2)

        disks_on_peg2 = []

        if whats_on_peg2:
            for x in whats_on_peg2:
                disks_on_peg2.append(int(x.bindings_dict['?x'].replace('disk', '')))

        disks_on_peg2.sort()

        # peg3: Checking what's on peg3
        on_peg3 = parse_input("fact: (on ?x peg3)")
        whats_on_peg3 = self.kb.kb_ask(on_peg3)

        disks_on_peg3 = []

        if whats_on_peg3:
            for x in whats_on_peg3:
                disks_on_peg3.append(int(x.bindings_dict['?x'].replace('disk', '')))

        disks_on_peg3.sort()

        return tuple(disks_on_peg1), tuple(disks_on_peg2), tuple(disks_on_peg3)

    def makeMove(self, movable_statement):

        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        if not(self.isMovableLegal(movable_statement)):
            pass
        else:
            use_to_match = self.produceMovableQuery()

            check = match(movable_statement, use_to_match.statement)
            if check:

                curr_disc = check.bindings[0].constant
                curr_init = check.bindings[1].constant
                curr_target = check.bindings[2].constant

                self.kb.kb_retract(parse_input('fact: (on '+curr_disc.element + ' ' + curr_init.element + ')'))
                self.kb.kb_retract(parse_input('fact: (top ' + curr_disc.element + ' ' + curr_init.element + ')'))

                check_above_curr = self.kb.kb_ask(parse_input('fact: (above '+curr_disc.element + ' ?x)'))

                if not check_above_curr:
                    self.kb.kb_assert(parse_input('fact: (empty '+curr_init.element+')'))
                else:
                    what_was_below = check_above_curr[0].bindings_dict['?x']
                    self.kb.kb_retract(parse_input('fact: (above '+curr_disc.element + ' ' + what_was_below + ')'))
                    self.kb.kb_assert(parse_input('fact: (top ' + what_was_below + ' ' + curr_init.element + ')'))

                check_empty_target = self.kb.kb_ask(parse_input('fact: (empty '+curr_target.element+')'))

                if check_empty_target:
                    self.kb.kb_retract(parse_input('fact: (empty '+curr_target.element+')'))
                    self.kb.kb_assert(parse_input('fact: (top ' + curr_disc.element + ' ' + curr_target.element + ')'))
                    self.kb.kb_assert(parse_input('fact: (on ' + curr_disc.element + ' ' + curr_target.element + ')'))
                else:
                    curr_target_top = self.kb.kb_ask(parse_input('fact: (top ?x '+curr_target.element+')'))
                    what_was_prev_top = curr_target_top[0].bindings_dict['?x']
                    self.kb.kb_retract(parse_input('fact: (top ' + what_was_prev_top + ' ' + curr_target.element + ')'))

                    # make new top
                    self.kb.kb_assert(parse_input('fact: (top ' + curr_disc.element + ' ' + curr_target.element))
                    self.kb.kb_assert(parse_input('fact: (above ' + curr_disc.element + ' ' + what_was_prev_top))
                    self.kb.kb_assert(parse_input('fact: (on ' + curr_disc.element + ' ' + curr_target.element + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        in_row1 = self.kb.kb_ask(parse_input("fact: (locy ?x pos1)"))
        tiles_in_row1 = [10, 10, 10]

        if in_row1:
            for x in in_row1:
                locx_of_x = self.kb.kb_ask(parse_input("fact: (locx " + x.bindings_dict['?x'] + " ?pos)"))
                posx_of_x = int(locx_of_x[0].bindings_dict['?pos'].replace('pos', '')) - 1
                if 'tile' in x.bindings_dict['?x']:
                    tiles_in_row1[posx_of_x] = (int(x.bindings_dict['?x'].replace('tile', '')))
                else:
                    tiles_in_row1[posx_of_x] = -1

        in_row2 = self.kb.kb_ask(parse_input("fact: (locy ?x pos2)"))
        tiles_in_row2 = [10, 10, 10]

        if in_row2:
            for x in in_row2:
                locx_of_x = self.kb.kb_ask(parse_input("fact: (locx " + x.bindings_dict['?x'] + " ?pos)"))
                posx_of_x = int(locx_of_x[0].bindings_dict['?pos'].replace('pos', '')) - 1
                if 'tile' in x.bindings_dict['?x']:
                    tiles_in_row2[posx_of_x] = (int(x.bindings_dict['?x'].replace('tile', '')))
                else:
                    tiles_in_row2[posx_of_x] = -1

        in_row3 = self.kb.kb_ask(parse_input("fact: (locy ?x pos3)"))
        tiles_in_row3 = [10, 10, 10]

        if in_row3:
            for x in in_row3:
                locx_of_x = self.kb.kb_ask(parse_input("fact: (locx " + x.bindings_dict['?x'] + " ?pos)"))
                posx_of_x = int(locx_of_x[0].bindings_dict['?pos'].replace('pos', '')) - 1
                if 'tile' in x.bindings_dict['?x']:
                    tiles_in_row3[posx_of_x] = (int(x.bindings_dict['?x'].replace('tile', '')))
                else:
                    tiles_in_row3[posx_of_x] = -1

        return tuple(tiles_in_row1), tuple(tiles_in_row2), tuple(tiles_in_row3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        if not (self.isMovableLegal(movable_statement)):
            pass
        else:
            used_for_match = self.produceMovableQuery()
            check = match(movable_statement, used_for_match.statement)

            if check:
                tile = check.bindings[0].constant
                currx = check.bindings[1].constant
                curry = check.bindings[2].constant
                futurex = check.bindings[3].constant
                futurey = check.bindings[4].constant

                self.kb.kb_retract(parse_input("fact: (locx empty " + futurex.element + ')'))
                self.kb.kb_retract(parse_input("fact: (locy empty " + futurey.element + ')'))
                self.kb.kb_retract(parse_input("fact: (locx " + tile.element + " " + currx.element + ')'))
                self.kb.kb_retract(parse_input("fact: (locy " + tile.element + " " + curry.element + ')'))

                self.kb.kb_assert(parse_input("fact: (locx empty " + currx.element + ')'))
                self.kb.kb_assert(parse_input("fact: (locy empty " + curry.element + ')'))
                self.kb.kb_assert(parse_input("fact: (locx " + tile.element + " " + futurex.element + ')'))
                self.kb.kb_assert(parse_input("fact: (locy " + tile.element + " " + futurey.element + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
