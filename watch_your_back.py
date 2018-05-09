###
# This Python class defines the rules of a game of Watch your back during
# the movement phase only.
###

from board_state import *
from copy import *
from collections import namedtuple
from move import generate_moves
from action import *

# This is namedtuple for quickly storing different attributes of a game state
GameState = namedtuple('GameState', 'to_move, utility, board_state, moves, '
                                    'turn_num')


class WatchYourBack:
    """
    This class is based off of the Game class from the libraries provided by
    the AIMA textbook
    """

    def __init__(self, start_state):

        # This refers to the initial game state at the beginning of the
        # movement phase
        # self.initial = GameState(to_move='O', utility=0, board_state=start_state,
        #                          moves=generate_moves(start_state, 'W'))
        self.initial_state = start_state

    def actions(self, state):
        """
        Function that gets the all of the possible moves from the current board
        state
        :param state:
        :return:
        """
        return state.moves

    def result(self, state, move):
        """

        :param state:
        :param move:
        :return:
        """
        output_board = deepcopy(state.board_state)
        move_action = Action(output_board, state.to_move, move=move)
        # Get the enemy piece
        if state.to_move == 'O':
            enemy = '@'
        else:
            enemy = 'O'
        # Now perform the action on the output_state
        output_board.modify(move_action, enemy)

        # Check if we have to shrink the board. Occurs at the end of turns
        # 127 and 191.
        if state.turn_num == 127:
            output_board.shrink_board()
        elif state.turn_num == 191:
            output_board.shrink_board()

        return GameState(to_move=enemy,
                         utility=self.compute_eval(output_board, enemy),
                         board_state=output_board,
                         moves=generate_moves(output_board, enemy),
                         turn_num=state.turn_num + 1)

    def cutoff_test(self):
        """
        This function determines whether to stop an Alpha Beta search if it has
        reached a certain condition. RIGHT NOW IT DOES NOTHING
        :return:
        """
        return None

    def terminal_test(self, state):
        """
        This function tests if a given board state is terminal. A state is
        terminal iff one side has 1 or less pieces or there are no empty squares
        left
        :param state:
        :return:
        """

        # Terminal test if there is only one piece left on our side or the enemy
        # side
        if len(state.board_state.search_board('W')) <= 1:
            return True
        elif len(state.board_state.search_board('B')) <= 1:
            return True
        elif len(state.board_state.search_board_char('-')) == 0:
            # No more empty spaces
            return True
        else:
            # Otherwise not a terminal state
            return False

    def to_move(self, state):
        """
        Return the player whose move it is in this state.
        :param state: The GameState object to check
        :return: A character corresponding to the player who will move for this
                 game state
        """
        return state.to_move

    def compute_eval(self, state, to_move):
        """
        This eval function can calculate a value using a few different ways
            - Subtract the current number of our pieces with the number of enemy pieces on
              the board. (This would be one feature)
            - Use the distances to goal tiles as previously implemented with massacre
            
        :param state:
        :param to_move: Character indicating whose turn it is for the current
                        state
        :return: 
        """
        # Getting the enemy character
        if to_move == 'O':
            enemy = '@'
        else:
            enemy = 'O'

        # Return the difference in our pieces
        return len(state.search_board_char(to_move)) - \
               len(state.search_board_char(enemy))





