###
# This Python module contains code for determining valid and smart movement
# actions to take during the movement phase of Watch your Back!
###

import random
from action import *
from move import generate_moves
from board_state import *
from minimax import *
from evaluation import *


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
                    move = Move(board_state, tile_list[y][0], tile_list[y][1], destination[0], destination[1])
                    return move


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
    if enemy == 'O':
        enemy = 'W'
    if len(temp_board_state.search_board(enemy)) == len(board_state.search_board(enemy)):
        return False
    return True


def check_easy_elimination(board_state, enemy, player):
    ''', move_list'''
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
    move_list = []
    # Get a list of all the current moves that the play could possibly make
    if enemy == '@':
        # If black is the enemy, then get poss_moves for white pieces
        poss_moves = generate_moves(board_state, 'W')
    else:
        # White is the enemy, possible moves for white
        poss_moves = generate_moves(board_state, 'B')
    action = None

    # Remove moves in list from poss_moves
    # poss_moves = [x for x in poss_moves if x not in move_list]

    if len(poss_moves) != 0:
        for move in poss_moves:
            if check_move_for_elimination(board_state, enemy, player, move):
                # print('CHECK')
                move_list.append(move)
                action = Action(board_state, enemy, action=None, move=move)
                break
        # Try move to centre
        move_list.append(move_to_centre_algorithm(board_state, enemy, player, poss_moves))
        # Random move
        move_list.append(poss_moves[random.randint(0, len(poss_moves)-1)])
    else:
        action = None

    return move_list


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

#-----------------------------------------------------------------#
'''
                    CAREFUL: UNDER CONSTRUCTION
                            ___
                     /======/
            ____    //      \___       ,/
             | \\  //           :,   ./
     |_______|__|_//            ;:; /
    _L_____________\o           ;;;/
____(CCCCCCCCCCCCCC)____________-/________________________________
'''
#-----------------------------------------------------------------#


class BoardTree(object):
    def __init__(self, breadth):
        self.parent = None
        self.first_child = None
        self.next_sibling = None
        self.board = None
        self.action_taken = None
        self.child = []



def evaluate_depth(board_state, enemy, player, depth, breadth):
    # Initialise root board state
    root_board = BoardTree()
    root_board.board = board_state

    move_list = []
    for x in range(depth):

        temp_action, temp_move = check_easy_elimination(board_state, enemy, player, move_list)

        next_board = BoardTree()
        next_board.board = temp_board_state.modify(temp_action, enemy)

        if root_board.first_child is None:
            root_board.first_child = next_board
            pass
        else:
            sibling = root_board.first_child
            while sibling.next_sibling is not None:
                sibling = sibling.next_sibling







        poss_moves = generate_move(root_board.board, enemy)
        if breadth > len(poss_moves):
            evalutation_range = len(poss_moves)
        else:
            evalutation_range = breadth






        for y in range(evalutation_range):
            temp_action, temp_move = check_easy_elimination(board_state, enemy, player, move_list)

            move_list.append(temp_move)

            temp_board_state = BoardState(None, root_board)

            next_board = BoardTree()
            # ?
            next_board.parent = root_board
            if root_board.first_child is None:
                next_board.first_child = temp_board_state.modify(temp_action, enemy)
            else:
                next_board.next_sibling = temp_board_state.modify(temp_action, enemy)

    action_list = []
    move_list = []
    f_list = []
    board_state_list = []

    for x in range(depth):
        action_list.append(x)
        move_list.append(x)
        f_list.append(x)
        board_state_list.append(x)
    max_f = 0
    # Tree "output : input"
    # For reverse traversal to find original input
    search_tree_of_board = {}
    key_count = 0

    for x in range(depth):
        poss_moves = generate_move(board_state, enemy)
        if breadth > len(poss_moves):
            evalutation_range = len(poss_moves)
        else:
            evalutation_range = breadth

        action_list[x] = []
        move_list[x] = []
        f_list[x] = []
        board_state_list[x] = []

        for y in range(evalutation_range):
            if x == 0:
                temp_action, temp_move = check_easy_elimination(board_state, enemy, player, move_list)
            else:
                temp_action, temp_move = check_easy_elimination(
                    search_tree_of_board.keys()[key_count], enemy, player, move_list)
                key_count += 1

            # This is inefficient
            move_list[x].append(temp_move)
            action_list[x].append(temp_action)

            # Evaluation
            temp_f = evalutate_this_move(list(search_tree_of_board.keys())[key_count], enemy, player, poss_moves[y])
            f_list[x].append(temp_f)

            # Store board states

            temp_board_state = BoardState(None, board_state)
            temp_board_state.modify(temp_action, enemy)
            # Just in case?
            board_error = False
            for board in board_state_list:
                if board is temp_board_state:
                    board_error = True
            if board_error is False:
                if x == 0:
                    search_tree_of_board[temp_board_state] = board_state, temp_action
                else:
                    search_tree_of_board[temp_board_state] = list(search_tree_of_board.keys())[key_count], temp_action

            board_state_list[x].append(temp_board_state)

    for x in range(len(f_list[len(f_list) - 1]) - 1, len(f_list[len(f_list) - 1]) - 1 - evalutation_range, -1):
        if f_list[len(f_list) - 1][x] > max_f:
            f_list[len(f_list) - 1][x] = max_f
            f_index = x

    traverse_board = list(search_tree_of_board.get(board_state_list[len(board_state_list) - 1]))[f_index]
    while search_tree_of_board.get(traverse_board) is not None:
        traverse_board = search_tree_of_board.get(traverse_board)

    return traverse_board[1]



