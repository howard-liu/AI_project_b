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
    'Watch your back' when used in the referee.py program. Serves as a baseline
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
        # Counter to store the number of turns the player has done since the
        # start of the game
        self.total_turns = 0

    def action(self, turns):
        """
        Method called by referee program to request an action from the player.
        :param turns:
        :return: A tuple if it is a placement action, a tuple of tuples if it is
                 a movement action and None if it is a forfeit action.
        """
        # Increment total turns every time this method is called
        self.total_turns += 1
        # Placing phase continues until we reach our 13th action
        if self.total_turns <= 12:
            action = do_random_place(self.board, self.enemy)
            self.board.modify(action, self.enemy)
        else:
            action = do_random_move(self.board, self.enemy)
            self.board.modify(action, self.enemy)
        # Consider the shrinking phases. Before the start of turns 128 and 192
        # So on turn 126 or 127, 190 or 191 depending on which player will be
        # the last chance to escape shrinkage etc.

        if action is None:
            return action
        else:
            return action.return_action()

    def update(self, action):
        """
        Method is called by referee to update the player's internal board
        representation with the most recent move done by the opponent
        :param action:
        :return:
        """
        # Placeholder to update the board from enemy perspective
        self.board.modify(Action(self.board, enemy=self.piece, action=action),
                          self.piece)
        return None
