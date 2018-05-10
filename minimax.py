###
# This Python file contains some experimental implementations of the Minimax
# algorithm based on the ones provided in AIMA textbook libraries
# They also contain custom variations made to suit the game of Watch your Back!
###

infinity = float('inf')


def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """
    Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Taken from AIMA textbook libraries
    :param state:
    :param game:
    :param d:
    :param cutoff_test:
    :param eval_fn:
    :return:
    """

    player = game.to_move(state)

    # Functions used by alphabetastat
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action
