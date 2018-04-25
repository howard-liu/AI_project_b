###
# This is the Player class that serves to decide and return which moves to do
# to perform to the referee program. This file will be the one that is marked
# for Part B of the project.
###

from board_state import *
from action import *
from placing_strategy import *
from moving_strategy import *


class Player:
    """
    Player class that is capable of playing a complete game of 'Watch your back'
    when used in the referee.py program
    """
    # Each player has 12 pieces
    TOTAL_PIECES = 12

    def __init__(self, colour):
        # Assign the character representing enemy pieces depending on the player
        # colour as well as what the player's piece is
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
        # TODO
        # Can't self.total_turns be replaced by turns (the input argument)?

        # Start off with a forfeited move and see if we can do anything
        action = None
        # Increment total turns every time this method is called
        self.total_turns += 1
        # Placing phase continues until we reach our 13th action
        if self.total_turns <= self.TOTAL_PIECES:
            action = do_random_place(self.board, self.enemy)
            self.board.modify(action, self.enemy)
        else:
            action = do_random_move(self.board, self.enemy)
            print(action.move)
            self.board.modify(action, self.enemy)
        # Consider the shrinking phases. Before the start of turns 128 and 192
        # So on turn 126 or 127, 190 or 191 depending on which player will be
        # the last chance to escape shrinkage etc.

        return action

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
