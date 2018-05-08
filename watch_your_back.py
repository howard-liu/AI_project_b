###
# This Python class defines the rules of a game of Watch your back during
# the movement phase only.
###

from board_state import *
from copy import *
from collections import namedtuple
from move import generate_moves

# This is namedtuple for quickly storing different attributes of a game state
GameState = namedtuple('GameState', 'to_move, utility, board_state, moves')


class WatchYourBack:
    """
    This class is based off of the Game class from the libraries provided by
    the AIMA textbook
    """

    def __init__(self, start_state):

        # This refers to the initial game state at the beginning of the
        # movement phase
        # TODO Create the evaluation function to evaluate the initial state of
        # the board at the beginning of a movement phase. This would then be
        # set as the utility value
        self.initial = GameState(to_move='O', utility=0, board_state=start_state,
                                 moves=generate_moves(start_state))

    def actions(self, state):
        """
        Function that gets the all of the possible moves from the current board
        state
        :param state:
        :return:
        """
        return state.moves

    def result(self, state, move):
        return

    def cutoff_test(self):
        return

    def compute_eval(self):
        return




