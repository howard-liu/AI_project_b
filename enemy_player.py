###
# This Python module will implement an enemy player class using a variety of
# different strategies. It's purpose is to serve as a baseline to benchmark
# our implemented Player class against to check performance. It's difficulty
# will be tweaked to use older strategies of our Player class whenever a new
# one is being tested.
###

from board_state import *
from placing_strategy import *
from moving_strategy import *


class Player:
    """
    Enemy player class that is also capable of playing a complete game of
    'Watch your back' when used in the referee_old.py program. Serves as a baseline
    to test Player class against.
    """
    def __init__(self, colour):
        # Assign the character representing enemy pieces depending on the colour
        #  as well as what the player's piece is
        if colour == 'white':
            self.enemy = '@'
            self.piece = 'O'
        else:
            self.enemy = 'O'
            self.piece = '@'
        # Create an empty board state to fill later
        self.board = BoardState()
        # Variable to fill in later to contain Game rules for moving phase
        self.game = None
        # Counter to store the number of turns the player has done since the
        # start of the game
        self.total_actions = 0
        # Variable that syncs the number of turns given by referee
        self.total_turns = 0
        # Variable to indicate which phase of the game we are in
        self.phase = 'placing'

    def action(self, turns):
        """
        Method called by referee program to request an action from the player.
        :param turns: Number of turns done so far in the current phase
        :return: A tuple if it is a placement action, a tuple of tuples if it is
                 a movement action and None if it is a forfeit action.
        """
        # Return the appropriate action depending on the phase

        if self.phase == 'placing':
            action = centre_place_strategy(self.board, self.enemy, self.piece)
            # action = do_random_place(self.board, self.enemy)
            self.board.modify(action, self.enemy)
        else:
            # We enter the movement phase of the game
            # action = check_easy_elimination(self.board, self.enemy, self.piece)
            # action = do_random_move(self.board, self.enemy)
            state = GameState(to_move=self.piece,
                              utility=self.game.compute_eval(self.board,
                                                             self.piece),
                              board_state=self.board,
                              moves=check_easy_elimination(self.board,
                                                           self.enemy,
                                                           self.piece),
                              turn_num=self.total_turns+1)
            action = tree_move(state, 2, 2, self.enemy)
            self.board.modify(action, self.enemy)

        # Increment total actions since we have played yet another action
        self.total_actions += 1
        # Sync turns
        self.total_turns = turns
        if self.phase == 'placing':
            if self.total_actions == 12:
                # Now switch to the moving phase
                self.phase = 'moving'
                # Reset turns
                self.total_turns = 0
                # Create the initial state of the game at the movement stage
                initial = GameState(to_move=self.enemy, utility=0,
                                    board_state=deepcopy(self.board),
                                    moves=check_easy_elimination(self.board,
                                                                 self.piece,
                                                                 self.enemy),
                                    turn_num=self.total_turns)
                self.game = WatchYourBack(initial)
        if self.phase == 'moving':
            # Check if we have to shrink the board. Occurs at the end of turns
            # 127 and 191.
            if self.total_turns == 127:
                self.board.shrink_board()
            elif self.total_turns == 191:
                self.board.shrink_board()

        if action is None:
            # Then this is a forfeited action
            return action
        else:
            return action.return_action()

    def update(self, action):
        """
        Method is called by referee to update the player's internal board
        representation with the most recent move done by the opponent
        :param action: A tuple representing the type of action that the opponent
                       did
        :return: None
        """
        # Increment to match the turns for the beginning of the next turn
        self.total_turns += 1
        # Update the board from enemy perspective
        self.board.modify(Action(self.board, enemy=self.piece, action=action),
                          self.piece)
        if self.phase == 'moving':
            # Check if we have to shrink the board for this current turn
            if self.total_turns == 127:
                self.board.shrink_board()
            elif self.total_turns == 191:
                self.board.shrink_board()

        return None
