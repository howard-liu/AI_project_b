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


def check_move_for_elimination(board_state, enemy, player, move):
    temp_board_state = BoardState(None, board_state)
    action = Action(board_state, enemy, action=None, move=move)
    temp_board_state.modify(action, enemy)
    if len(temp_board_state.search_board(enemy)) == len(board_state.search_board(enemy)):
        # print('Lalalalalalalalalalalalalalalalalalalala')
        return False
    # print('YOOYOYOYOYOYOYOYOYOYOYOYOYOYOYOYOYOYOYOYOYO')
    return True


def check_easy_elimination(board_state, enemy, player):
    # Get a list of all the current moves that the play could possibly make
    if enemy == '@':
        # If black is the enemy, then get poss_moves for white pieces
        poss_moves = generate_moves(board_state, 'W')
    else:
        # White is the enemy
        poss_moves = generate_moves(board_state, 'B')

    move = poss_moves[random.randint(0, len(poss_moves)-1)]
    action = Action(board_state, enemy, action=None, move=move)

    if len(poss_moves) != 0:
        for move in poss_moves:
            if check_move_for_elimination(board_state, enemy, player, move):
                # print('CHECK')
                action = Action(board_state, enemy, action=None, move=move)
                break
    else:
        action = None

    return action
