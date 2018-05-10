###
# This Python file contains some experimental implementations of the Minimax
# algorithm based on the ones provided in AIMA textbook libraries
# This was used to experiment with how well minimax and alphabeta etc. would
# perform.
###

infinity = float('inf')


def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """
    Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Taken from AIMA textbook libraries
    :param state: A namedtuple GameState containing attributes of a game state
    :param game: A WatchYourBack game object representing the rules of the game
                 during the movement phase only
    :param d: An integer referring to the depth to search to
    :param cutoff_test: Defaults to None. Specified only if you want to cutoff
                        the search in another way that does not use depth
    :param eval_fn: The evaluation function used to determine how good a state is
    :return: The best action to perform according to alpha beta search
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
