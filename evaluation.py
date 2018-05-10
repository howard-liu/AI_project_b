###
# This Python file contains different evaluation functions to determine how
# good a given board configuration is for the specified piece
###

from move import *


def count_matching_goal(goal_spots, piece_locs):

    num_match = 0
    # Count up all the pieces that are on a goal spot.
    for p in piece_locs:
        if p in goal_spots:
            num_match += 1

    return num_match


def distance_between(j, i, y, x):
    """
    This function finds the distance two points
    :param j: Coordinates
    :param i: Coordinates
    :param y: Coordinates
    :param x: Coordinates
    :return: distance between points
    """
    return abs(j - y) + abs(i - x)


def inverse_sum_distances(piece_locs, goal_spots):
    """
    This function sums the distances to the closest goal tiles for each piece
    not already on a goal tile. It then inverses this sum, so that the smaller
    the distances are, the greater the value returned will be
    :param piece_locs:
    :param goal_spots:
    :return:
    """

    total = 0

    for p in piece_locs:
        # Starting with a high value to minimise
        min_dist = float('inf')
        if p not in goal_spots:
            for goal in goal_spots:
                curr_dist = distance_between(p[0], p[1], goal[0], goal[1])
                if curr_dist < min_dist:
                    min_dist = curr_dist
            total += min_dist

    # Return the inverse of the total. The greater the distances between all of
    # the pieces the greater the total
    if total != 0:
        return 1/total
    else:
        return 0


def diff_piece(board_state, piece):
    """
    This function returns the difference in number between our pieces and the
    enemies
    :param board_state:
    :param piece:
    :return:
    """
    if piece == 'O':
        enemy = '@'
    else:
        enemy = 'O'

    return len(board_state.search_board_char(piece)) - \
           len(board_state.search_board_char(enemy))


def eval_fn(game_state):
    """
    The function that will return an approximation of how good a current state
    is
    :return:
    """
    piece = game_state.to_move
    board_state = game_state.board_state

    # These variables contain the weights for the 3 features used
    alpha = 3.0
    beta = 2.0
    gamma = 1.0

    piece_locs = board_state.search_board_char(piece)
    goal_spots = find_goal_tiles(board_state, piece)

    match = count_matching_goal(goal_spots, piece_locs)
    dist = inverse_sum_distances(piece_locs, goal_spots)
    diff = diff_piece(board_state, piece)

    return (alpha*diff) + (beta*match) + (gamma*dist)
