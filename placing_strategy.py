###
# This Python module contains the code that will determine which placing actions
# take during the placing phase.
###

import random
from action import *
from board_state import *


# MAX number of attempts to check before giving up
MAX_ATTEMPTS = 10


def do_random_place(board_state, enemy):
    """
    Function that will do random placement actions
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :return: An action or None if it is forfeited action
    """

    action = None
    attempts = 0
    while action is None and attempts < MAX_ATTEMPTS:
        try:
            col = random.randint(0, 7)
            row = random.randint(0, 7)
            action = Action(board_state, enemy, action=(col, row))
            attempts += 1
        except InvalidMoveError:
            pass

    if action is None:
        print("ERROR: NO VALID ACTION FOUND")
        exit()
    else:
        return action


def first_move(board_state, enemy):
    """
    First move strategy as a test/baseline of a centre-focused strat
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :return: An action or None if it is forfeited action
    """
    # Centre pieces are (3,3),(3,4),(4,3),(4,4)
    if board_state.output_piece(3, 4) == enemy:
        col = 4
        row = 3
    elif board_state.output_piece(4, 3) == enemy:
        col = 3
        row = 4
    else:
        if board_state.output_piece(3, 3) == '-':
            row = 3
            col = 3
        elif board_state.output_piece(3, 4) == '-':
            row = 3
            col = 4
        elif board_state.output_piece(4, 3) == '-':
            row = 4
            col = 3
        elif board_state.output_piece(4, 4) == '-':
            row = 4
            col = 4
    action = Action(board_state, enemy, action=(col, row))
    return action

# def second_move(board_state, enemy):
    # First check if can immediately kill a piece
    # If not find a centre piece which does not commit suicide


# Enter in a rank (between 1 to 4) and it will give out list of tuples
def tiles_ranking(rank):
    tile_ranking_dictionary = {
        0: 1,
        1: 2,
        2: 3,
        3: 4,
        4: 4,
        5: 3,
        6: 2,
        7: 1
    }
    tuples = []
    for x in range(7):
        for y in range(7):
            if min(tile_ranking_dictionary[x], tile_ranking_dictionary[y]) == rank:
                tuples.append((x, y))
    return tuples


