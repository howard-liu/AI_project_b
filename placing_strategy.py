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
        return None
    return col, row - 1


def look_down(col, row):
    if row == 7:
        return None
    return col, row + 1


def look_left(col, row):
    if col == 0:
        return None
    return col - 1, row


def look_right(col, row):
    if col == 7:
        return None
    return col + 1, row

# </Helper functions for blacklist_bad_tiles() that are sort of duplicated and can be moved if there is time>


def find_tiles_of_rank(rank):
    """
    Enter in rank (0-3) (3 is centre) and it will output a list of tuples that
    are in that circular level of the board
    :param rank: Int 0 to 3, where 3 is the centre, 0 is the outermost tiles
    :return: List of tuples that are in that level
    """
    tile_dict = {0: [
                     (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                     (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
                     (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
                     (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)
                    ],
                 1: [
                     (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                     (2, 1), (3, 1), (4, 1), (5, 1),
                     (2, 6), (3, 6), (4, 6), (5, 6),
                     (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)
                    ],
                 2: [
                     (2, 2), (2, 3), (2, 4), (2, 5),
                     (3, 2), (4, 2),
                     (3, 5), (4, 5),
                     (5, 2), (5, 3), (5, 4), (5, 5)
                    ],
                 3: [
                     (3, 3), (3, 4),
                     (4, 3), (4, 4)
                    ]
                 }

    return tile_dict[rank]


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
        # r = list(range(len(tile_list)))
        for y in range(len(tile_list)):
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


def find_bad_spots(board_state, piece):
    """
    This function finds the spots that are considered bad to place on.
    :param board_state:
    :param piece:
    :return: A list of tuples that represent tiles that our pieces should not
             be placed on
    """
    black_list = []
    # Get enemy character
    if piece == 'O':
        enemy = '@'
    else:
        enemy = 'O'

    # Search across all the enemy pieces on the board
    for col, row in board_state.search_board_char(enemy):
        check_bad_spot_piece(board_state, black_list, col, row, piece)

    # Convert into set to remove duplicates and then return as list
    return list(set(black_list))


def check_bad_spot_piece(board_state, black_list, col, row, player):
    """
    This function highlights the spots around an enemy piece that would be
    considered bad to place on. These spots are bad if:
        - They are directly next to the enemy piece unless if placing next to
          the enemy piece would allow our piece to kill it
    :param board_state:
    :param black_list:
    :param col:
    :param row:
    :param player:
    :return:
    """
    # Tuple storing pieces that can eliminate the enemy piece
    killer = ('X', player)

    # Checking above and below the piece
    if row-1 >= board_state.min_row and row+1 <= board_state.max_row:
        # Check if there is one of our pieces, that would allow us to kill this
        # enemy piece
        if board_state.board[col][row+1] not in killer:
            black_list.append((col, row-1))
        # Now checking below
        if board_state.board[col][row-1] not in killer:
            black_list.append((col, row+1))

    # Checking to the left of the piece
    if col-1 >= board_state.min_col and col+1 <= board_state.max_col:
        # Check if there is one of our pieces, that would allow us to kill this
        # enemy piece
        if board_state.board[col+1][row] not in killer:
            black_list.append((col-1, row))
        # Checking to the right of the piece now
        if board_state.board[col-1][row] not in killer:
            black_list.append((col+1, row))
    return


def defend_piece(board_state, enemy, player):
    enemy_list = []

    for x in range(3, 0, -1):
        tile_list = find_tiles_of_rank(x)
        r = list(range(len(tile_list)))
        for y in r:
            if board_state.output_piece(tile_list[y][0], tile_list[y][1]) == enemy:
                for tile in tile_list:
                    enemy_list.append(tile)

    for enemy_tile in enemy_list:
        # print('ENEMY TILE: ' + str(enemy_tile))
        down = look_down(enemy_tile[0], enemy_tile[1])
        up = look_up(enemy_tile[0], enemy_tile[1])
        left = look_left(enemy_tile[0], enemy_tile[1])
        right = look_right(enemy_tile[0], enemy_tile[1])

        if down is not None:
            if board_state.output_piece(down[0], down[1]) == enemy:
                down_two = look_down(down[0], down[1])
                if down_two is not None:
                    if board_state.output_piece(down_two[0], down_two[1]) == player:
                        down_three = look_down(down_two[0], down_two[1])
                        if down_three is not None:
                            if board_state.output_piece(down_three[0], down_three[1]) == '-':
                                return down_three[0], down_three[1]

        if up is not None:
            if board_state.output_piece(up[0], up[1]) == enemy:
                up_two = look_up(up[0], up[1])
                if up_two is not None:
                    if board_state.output_piece(up_two[0], up_two[1]) == player:
                        up_three = look_up(up_two[0], up_two[1])
                        if up_three is not None:
                            if board_state.output_piece(up_three[0], up_three[1]) == '-':
                                return up_three[0], up_three[1]

        if left is not None:
            if board_state.output_piece(left[0], left[1]) == enemy:
                left_two = look_left(left[0], left[1])
                if left_two is not None:
                    if board_state.output_piece(left_two[0], left_two[1]) == player:
                        left_three = look_left(left_two[0], left_two[1])
                        if left_three is not None:
                            if board_state.output_piece(left_three[0], left_three[1]) == '-':
                                return left_three[0], left_three[1]

        if right is not None:
            if board_state.output_piece(right[0], right[1]) == enemy:
                right_two = look_right(right[0], right[1])
                if right_two is not None:
                    if board_state.output_piece(right_two[0], right_two[1]) == player:
                        right_three = look_right(right_two[0], right_two[1])
                        if right_three is not None:
                            if board_state.output_piece(right_three[0], right_three[1]) == '-':
                                return right_three[0], right_three[1]

    return None


def centre_place_strategy(board_state, enemy, player):
    """
    Simple strategy that prioritises centre tiles
    - If there is a place that can eliminate an enemy piece, it will do it
    - Does not place at squares next to an enemy piece (enemy can take the
      next turn)
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :param player: Character representing the player piece
    :return: An action
    """
    min_row = board_state.min_row
    max_row = board_state.max_row
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

    black_listed_tiles = find_bad_spots(board_state, player)

    def_move = defend_piece(board_state, enemy, player)
    if def_move is not None and min_row <= def_move[1] <= max_row:
        if def_move not in black_listed_tiles:
            action = Action(board_state, enemy, action=(def_move[0], def_move[1]))
            print('ACTION: ' + str(def_move))
            return action

    for x in range(3, 0, -1):
        temp_tile_list = find_tiles_of_rank(x)
        tile_list = []
        for tile in temp_tile_list:
            if min_row <= tile[1] <= max_row:
                tile_list.append(tile)
        r = list(range(len(tile_list)))
        # Shuffle the indices
        random.shuffle(r)
        for y in r:
            if board_state.output_piece(tile_list[y][0], tile_list[y][1]) == '-':
                if tile_list[y] not in black_listed_tiles:
                    action = Action(board_state, enemy, action=(tile_list[y][0], tile_list[y][1]))
                    if action is not None:
                        return action
    # otherwise just do a random move
    return do_random_place(board_state, enemy)


