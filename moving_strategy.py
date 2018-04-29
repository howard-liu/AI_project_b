###
# This Python module contains code for determining valid and smart movement
# actions to take during the movement phase of Watch your Back!
###

import random
from action import *
from move import generate_moves
from board_state import *


def do_random_move(board_state, enemy):
    """
    Function that will do random placement actions
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :return: An action or None if it is forfeited action
    """
    # Get a list of all the current moves that the play could possibly make
    if enemy == '@':
        # If black is the enemy, then get poss_moves for white pieces
        poss_moves = generate_moves(board_state, 'W')
    else:
        # White is the enemy
        poss_moves = generate_moves(board_state, 'B')

    # Pick a random move to do if there is a valid one
    if len(poss_moves) != 0:
        move = poss_moves[random.randint(0, len(poss_moves)-1)]
        action = Action(board_state, enemy, action=None, move=move)
    else:
        # This is a forfeited action. There are no possible moves.
        action = None

    return action

# Copied from placing_strategy
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


def move_towards_centre(board_state, col, row, enemy):
    """
    Outputs tuple, destination of moving a piece towards the centre
    :param board_state: The current state of the board
    :param col: Column of the piece we may be moving
    :param row: Row of the piece we may be moving
    :param enemy: Enemy piece
    :return: Tuple of destination of move, or none if not found
    """
    new_row = row
    new_col = col
    if col > 5:
        new_col = col - 1
    elif col < 3:
        new_col = col + 1
    if new_col != col:
        try:
            Move(board_state, col, row, new_col, new_row)
        except InvalidMoveError:
            return None
        return new_col, new_row

    if row > 5:
        new_row = row - 1
    elif row < 3:
        new_row = row + 1
    if new_row != row:
        try:
            Move(board_state, col, row, new_col, new_row)
        except InvalidMoveError:
            return None
        return new_col, new_row

    return None


def move_to_centre_algorithm(board_state, enemy, player, possmoves):
    """
    An algorithm that moves pieces towards the centre, starting from the outermost area
    This is strong because it means that we can stall until the board shrinks
    And take advantage of opponent's stupid moves
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :param player: Character representing the player piece
    :return: An action
    """
    # Outside in
    for x in range(3):
        tile_list = find_tiles_of_rank(x)
        r = list(range(len(tile_list)))
        # random.shuffle(r)
        for y in r:
            if board_state.output_piece(tile_list[y][0], tile_list[y][1]) == player:
                destination = move_towards_centre(board_state, tile_list[y][0], tile_list[y][1], enemy)
                if destination is not None:
                    print(tile_list[y])
                    print(destination)
                    move = Move(board_state, tile_list[y][0], tile_list[y][1], destination[0], destination[1])
                    action = Action(board_state, enemy, action=None, move=move)
                    return action


def check_move_for_elimination(board_state, enemy, player, move):
    """
    Tests a move to see whether it eliminates an enemy piece
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :param player: Character representing the player piece
    :param move: The move that is being tested
    :return: Does it eliminate a piece? Boolean
    """
    temp_board_state = BoardState(None, board_state)
    action = Action(board_state, enemy, action=None, move=move)
    temp_board_state.modify(action, enemy)
    if len(temp_board_state.search_board(enemy)) == len(board_state.search_board(enemy)):
        return False
    return True


def check_easy_elimination(board_state, enemy, player):
    """
    Simple strategy:
    - Check for 1 move elimination
    - Else, move pieces towards the centre from the outermost pieces
    - Else, do a random move
    :param board_state: The current state of the board
    :param enemy: Character representing the enemy piece
    :param player: Character representing the player piece
    :return: An action
    """
    # Get a list of all the current moves that the play could possibly make
    if enemy == '@':
        # If black is the enemy, then get poss_moves for white pieces
        poss_moves = generate_moves(board_state, 'W')
    else:
        # White is the enemy
        poss_moves = generate_moves(board_state, 'B')
    action = None

    if len(poss_moves) != 0:
        for move in poss_moves:
            if check_move_for_elimination(board_state, enemy, player, move):
                print('CHECK')
                action = Action(board_state, enemy, action=None, move=move)
                break
        if action is None:
            # Try move to centre
            action = move_to_centre_algorithm(board_state, enemy, player, poss_moves)
            if action is None:
                # Random move
                move = poss_moves[random.randint(0, len(poss_moves)-1)]
                action = Action(board_state, enemy, action=None, move=move)
    else:
        action = None

    return action
