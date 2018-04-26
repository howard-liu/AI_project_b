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


def find_tiles_of_rank(rank):
    """
    Enter in rank (0-3) (3 is centre) and it will spit out a list of tuples that are in that rank
    :param rank: Int 0 to 3, where 3 is the centre, 0 is the outermost tiles
    :return: List of tuples that are in the rank
    """
    tile_rank = [([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 7),(2, 0), (2, 7), (3, 0), (3, 7),
                   (4, 0), (4, 7), (5, 0), (5, 7), (6, 0), (6, 7), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)]),
                 ([(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 1), (2, 6), (3, 1), (3, 6),
                   (4, 1), (4, 6), (5, 1), (5, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]),
                 ([(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 5), (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]),
                 ([(3, 3), (3, 4), (4, 3), (4, 4)])]

    return tile_rank[rank]

# <Helper functions for blacklist_bad_tiles() that are sort of duplicated and can be moved if there is time>


def look_up(col, row):
    return col, row - 1


def look_down(col, row):
    return col, row + 1


def look_left(col, row):
    return col - 1, row


def look_right(col, row):
    return col + 1, row

# </Helper functions for blacklist_bad_tiles() that are sort of duplicated and can be moved if there is time>


# TODO
# Except for possible to take pieces
def blacklist_bad_tiles(board_state, enemy):
    """
    Checks up, down, left, right of all enemy tiles to give a list of 'blacklisted' tiles
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :return: List of tuples that should not be placed
    """
    enemy_tiles = board_state.search_board(enemy)
    tile_list = []
    for enemy_tile in enemy_tiles:
        tile_list.append(look_down(enemy_tile[0], enemy_tile[1]))
        tile_list.append(look_up(enemy_tile[0], enemy_tile[1]))
        tile_list.append(look_left(enemy_tile[0], enemy_tile[1]))
        tile_list.append(look_right(enemy_tile[0], enemy_tile[1]))

 
def centre_place_strategy(board_state, enemy):
    """
    Simple blind strategy that places pieces from the centre
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :return: An action
    """
    for x in range(3, 0, -1):
        tile_list = find_tiles_of_rank(x)
        r = list(range(len(tile_list)))
        random.shuffle(r)
        for y in r:
            if board_state.output_piece(tile_list[y][0], tile_list[y][1]) == '-':
                action = Action(board_state, enemy, action=(tile_list[y][0], tile_list[y][1]))
                return action

        # while len(tile_list) > 0:
        #     tile = random.choice(tile_list)
        #     if board_state.output_piece(tile[0], tile[1]) == '-':
        #         action = Action(board_state, enemy, action=(tile[0], tile[1]))
        #         return action

