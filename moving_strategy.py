###
# This Python module contains code for determining valid and smart movement
# actions to take during the movement phase of Watch your Back!
###

import random
from minimax import *
from board_tree import *
from move_generator import *


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


def do_alphabeta_action(state, game):
    """
    This function uses the Alpha Beta algorithm with a depth cutoff, to return
    the best action advised by the evaluation function
    :param state: A GameState object
    :param game: A WatchYourBack game representing the rules of the game during
                 the movement phase
    :return:
    """
    best_move = alphabeta_cutoff_search(state, game, d=4, eval_fn=eval_fn)

    # Getting the enemy character
    if state.to_move == 'O':
        enemy = '@'
    else:
        enemy = 'O'

    # Convert to an action and return
    return Action(state.board_state, enemy, action=None, move=best_move)


def evalutate_this_move(board_state, enemy, player, move):
    temp_board_state = BoardState(None, board_state)
    action = Action(board_state, enemy, action=None, move=move)
    temp_board_state.modify(action, enemy)
    if enemy == 'O':
        enemy = 'W'
    return len(temp_board_state.search_board(player)) - len(board_state.search_board(enemy))


def generate_move(board_state, enemy):
    # Generate possible move
    # Get a list of all the current moves that the play could possibly make
    if enemy == '@':
        # If black is the enemy, then get poss_moves for white pieces
        poss_moves = generate_moves(board_state, 'W')
    else:
        # White is the enemy, possible moves for white
        poss_moves = generate_moves(board_state, 'B')
    return poss_moves


def tree_move(state, d, b, enemy):
    """
    This function will look ahead a few moves, and then pick the move that may
    lead us down the best choice
    :param state:
    :param d:
    :param b:
    :param enemy:
    :return:
    """

    # Create a board tree with the specified depth and breadth from the
    # given state
    tree = BoardTree(state, d, b)
    leaf_nodes = tree.leafs
    # Start from a really low score, to find the highest
    eval_score = -float('inf')
    optimal_node = None

    # Search for the best leaf node
    for node in leaf_nodes:
        if eval_fn(node.game_state) > eval_score:
            optimal_node = node

    return Action(state.board_state,  enemy, move=optimal_node.solution()[0])