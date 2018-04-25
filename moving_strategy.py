###
# This Python module contains code for determining valid and smart movement
# actions to take during the movement phase of Watch your Back!
###

import random
from action import *
from move import generate_moves


# MAX number of attempts to check before giving up
MAX_ATTEMPTS = 100


def do_random_move(board_state, enemy):
    """
    Function that will do random placement actions
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :return: An action or None if it is forfeited action
    """
    # Get a list of the current pieces on the board
    if enemy == '@':
        # Enemy is black, so search for white pieces on the board
        pieces = board_state.search_board('W')
    else:
        # Search for black pieces
        pieces = board_state.search_board('B')

    # Now pick a random piece to move
    piece_ind = random.randint(0, len(pieces))

    action = None
    attempts = 0
    while action is None and attempts < MAX_ATTEMPTS:
        try:
            col = random.randint(0, 7)
            row = random.randint(0, 7)
            action = Action(board_state, (col, row), enemy)
            attempts += 1
        except InvalidMoveError:
            pass

    if action is None:
        print("ERROR: NO VALID VALUE FOUND")
        exit()
    else:
        return action

    return