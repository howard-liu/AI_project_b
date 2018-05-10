###
# This Python module contains the code that will determine which placing actions
# take during the placing phase.
###

import random
from action import *
from move import is_suicide
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


# <Helper functions for blacklist_bad_tiles() that are sort of duplicated and can be moved if there is time>

# Shitty wrap fix
def look_up(col, row):
    if row == 0:
        return col, row # None
    return col, row - 1


def look_down(col, row):
    if row == 7:
        return col, row
    return col, row + 1


def look_left(col, row):
    if col == 0:
        return col, row
    return col - 1, row


def look_right(col, row):
    if col == 7:
        return col, row
    return col + 1, row

# </Helper functions for blacklist_bad_tiles() that are sort of duplicated and can be moved if there is time>


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


# Find positions of enemy
# For each positions of enemy
# Check up down left right for non-enemy, non-blank pieces
# If found, place at the opposite side

# TODO
# Update blacklist with safe squares (my piece may be protected from behind)
# Check for suicide before placing

def priority_eliminate(board_state, enemy, player):
    """
    If there is a piece that player can eliminate, output the tuple of move that will do it
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :return: An action or None if no elimination can be done
    """
    # Priorities the centre, because it is more valuable in the future
    for x in range(3, 0, -1):
        tile_list = find_tiles_of_rank(x)
        r = list(range(len(tile_list)))
        for y in r:
            if board_state.output_piece(tile_list[y][0], tile_list[y][1]) == enemy:
                # Check down
                down = look_down(tile_list[y][0], tile_list[y][1])
                up = look_up(tile_list[y][0], tile_list[y][1])
                if board_state.output_piece(up[0], up[1]) == '-':
                    while board_state.output_piece(down[0], down[1]) not in [enemy, '-']:
                        return look_up(tile_list[y][0], tile_list[y][1])
                # Check up
                if board_state.output_piece(down[0], down[1]) == '-':
                    while board_state.output_piece(up[0], up[1]) not in [enemy, '-']:
                        return look_down(tile_list[y][0], tile_list[y][1])
                # Check left
                left = look_left(tile_list[y][0], tile_list[y][1])
                right = look_right(tile_list[y][0], tile_list[y][1])
                if board_state.output_piece(right[0], right[1]) == '-':
                    while board_state.output_piece(left[0], left[1]) not in [enemy, '-']:
                        return look_right(tile_list[y][0], tile_list[y][1])
                # Check right
                if board_state.output_piece(left[0], left[1]) == '-':
                    while board_state.output_piece(right[0], right[1]) not in [enemy, '-']:
                        return look_left(tile_list[y][0], tile_list[y][1])
    return None


def blacklist_bad_tiles(board_state, enemy, player):
    """
    Checks up, down, left, right of all enemy tiles to give a list of 'blacklisted' tiles
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :param player:
    :return: List of tuples that should not be placed
    """
    if enemy == 'O':
        player = 'W'
    else:
        player = 'O'
    enemy_tiles = board_state.search_board(enemy)
    tile_list = []
    for enemy_tile in enemy_tiles:

        down = look_down(enemy_tile[0], enemy_tile[1])
        up = look_up(enemy_tile[0], enemy_tile[1])
        left = look_left(enemy_tile[0], enemy_tile[1])
        right = look_right(enemy_tile[0], enemy_tile[1])

        down_down = None
        up_up = None
        left_left = None
        right_right = None

        if down is not None:
            down_down = look_down(down[0], down[1])
        if up is not None:
            up_up = look_up(up[0], up[1])
        if left is not None:
            left_left = look_left(left[0], left[1])
        if right_right is not None:
            right_right = look_right(right[0], right[1])

        if down_down is not None:
            if board_state.output_piece(down_down[0], down_down[1]) != player:
                tile_list.append(look_down(enemy_tile[0], enemy_tile[1]))
        if up_up is not None:
            if board_state.output_piece(up_up[0], up_up[1]) != player:
                tile_list.append(look_up(enemy_tile[0], enemy_tile[1]))
        if left_left is not None:
            if board_state.output_piece(left_left[0], left_left[1]) != player:
                tile_list.append(look_left(enemy_tile[0], enemy_tile[1]))
        if right_right is not None:
            if board_state.output_piece(right_right[0], right_right[1]) != player:
                tile_list.append(look_right(enemy_tile[0], enemy_tile[1]))
    return tile_list


def is_not_in_list(list_of_tiles, tile):
    """
    Compares a tile against a list of tiles
    :param list_of_tiles: A list of tiles (blacklist)
    :param tile: A tile to compare with
    :return: Whether the tile is in the list of (blacklisted) tiles
    """
    for z in list_of_tiles:
        # print(tile)
        # print(z)
        if tile == z:
            # print('Check')
            return False
    return True


def centre_place_strategy(board_state, enemy, player):
    """
    Simple strategy that prioritises centre tiles
    - If there is a place that can eliminate an enemy piece, it will do it
    - Does not place at squares next to an enemy piece (enemy can take the next turn)
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :param player: Character representing the player piece
    :return: An action
    """
    min_row = 0
    max_row = 7
    # If our player is using black pieces
    if player == 'O':
        max_row = 5
    # If our player is using white pieces
    elif player == '@':
        min_row = 2
    kill_tile = priority_eliminate(board_state, enemy, player)
    if kill_tile is not None and min_row <= kill_tile[1] <= max_row:
        # print('Killtile: ' + str(kill_tile[0]) + ',' + str(kill_tile[1]))
        action = Action(board_state, enemy, action=(kill_tile[0], kill_tile[1]))
        return action
    for x in range(3, 0, -1):
        # print(x)
        temp_tile_list = find_tiles_of_rank(x)
        tile_list = []
        for tile in temp_tile_list:
            if min_row <= tile[1] <= max_row:
                tile_list.append(tile)
        r = list(range(len(tile_list)))
        random.shuffle(r)
        for y in r:
            if board_state.output_piece(tile_list[y][0], tile_list[y][1]) == '-':
                black_listed_tiles = blacklist_bad_tiles(board_state, enemy, player)
                # if player == '@':
                #     print(black_listed_tiles)
                if is_not_in_list(black_listed_tiles, tile_list[y]):
                    # For testing (DELETE WHEN RESOLVED)
                    # print('action to be: ' + str((tile_list[y][0], tile_list[y][1])))
                    action = Action(board_state, enemy, action=(tile_list[y][0], tile_list[y][1]))
                    # For testing (DELETE WHEN RESOLVED)
                    # print('action: ' + str(action))
                    if action is not None:
                        return action
    return None


