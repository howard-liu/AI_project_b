###
# Python module that contains classes and functions that represent the moves
# in the board game "Watch your back!".
###


# A simple little custom exception to raise whenever an invalid move is passed
class InvalidMoveError(Exception):
    pass


class Move:
    """
    This class represents a valid move in the game "Watch your Back!"
    """
    def __init__(self, board_state, col=None, row=None, new_col=None,
                 new_row=None, enemy=None):
        """
        A move object contains the coordinates of the piece to be moved as well
        as the coordinates of the new location that the piece will be moved to
         :param board_state: BoardState object containing information about the
                            current state of the game
        :param col: The column number this move refers to. Defaults to None
        :param row: The row number this move refers to. Defaults to None
        :param new_col: The new column number this move will place the piece to.
                        Defaults to None when the move is a placing move.
        :param new_row: The new row number this move will place the piece to.
                        Defaults to None when this move is a placing move.
        :param enemy: A character that represents an enemy piece on the board.
                      Defaults to None if no character is specified.
        """

        # Check if the move is valid before creating the object
        self.curr_col = col
        self.curr_row = row
        self.new_col = new_col
        self.new_row = new_row
        if not self.__is_place__(board_state, col, row, new_col, new_row,
                                 enemy) and \
                not self.__is_move__(board_state, col, row, new_col, new_row):
            error = "Invalid Move detected, attempted: ({}, {}) -> ({}, {})".format(
                self.curr_col, self.curr_row, self.new_col, self.new_row)
            raise InvalidMoveError(error)

    def __eq__(self, other):
        """
        Function to test if the current move is equal to another one
        :param other: The other object to check against
        :return: True if they are the same and False otherwise
        """
        if self is other:
            return True
        elif type(self) != type(other):
            return False
        else:
            # Compare if all values are the same
            if self.curr_col == other.curr_col and \
               self.curr_row == other.curr_row and \
               self.new_col == other.new_col and \
               self.new_row == other.new_row:
                return True
            else:
                # Otherwise they must be a different move
                return False

    def __hash__(self):
        return hash((self.curr_col, self.curr_row, self.new_col, self.new_row))

    def __str__(self):
        """
        To string function that prints out what the move is
        :return: None
        """
        line = "({}, {}) -> ({}, {})".format(self.curr_col, self.curr_row,
                                             self.new_col, self.new_row)
        return line

    @classmethod
    def __is_place__(cls, board_state, col, row, new_col, new_row, enemy):
        """
        This method checks if the current move is a placing one or not. If it is
        a placing move then it checks if it is a valid placement.
        :param col: Column number to check
        :param row: Row number to check
        :param new_col: New column number to check to see if it is None.
        :param new_row: New row number to check to see if it is None.
        :param enemy: Character representing the enemy pieces. Also checks to
                      see if None was placed.
        :return: True if the move is a valid placement move. Otherwise returns
                 False.
        """
        # Check these values if one comes back as true then return False.
        if new_col is not None or new_row is not None or enemy is None:
            return False
        # Now proceed to check if the coordinates specified are valid
        if col is None or row is None:
            return False
        # Variables to determine the range of rows that white or black players
        # are allowed to place their pieces onto
        min_row = 0
        max_row = 7
        # If our player is using black pieces
        if enemy == '@':
            max_row = 5
        # If our player is using white pieces
        elif enemy == 'O':
            min_row = 2

        if min_row <= row <= max_row:
            # Now check that the space is not occupied and is also not a corner
            # location
            if board_state.board[col][row] == '-':
                return True
        # Otherwise not a valid placing move
        return False

    @classmethod
    def __is_move__(cls, board_state, col, row, new_col, new_row):
        """
        This function checks if the current movement move being created is valid
        :param board_state: The current state of the board
        :param col: Column number to check
        :param row: Row number to check
        :param new_col: New column number to check to see
        :param new_row: New row number to check to see
        :return: True if the move is valid and False otherwise
        """
        # If either of these values don't exist, then it is not a movement move
        if new_col is None or new_row is None:
            return False

        # Check if the current coords refer to an actual piece
        if board_state.board[col][row] != 'O' and \
           board_state.board[col][row] != '@':
            return False
        else:
            # Check if the new coords are valid
            validity = False
            out = cls.check_up(board_state, col, row)
            if out:
                if out[0] == new_col and out[1] == new_row:
                    validity = True
            out = cls.check_down(board_state, col, row)
            if out:
                if out[0] == new_col and out[1] == new_row:
                    validity = True
            out = cls.check_left(board_state, col, row)
            if out:
                if out[0] == new_col and out[1] == new_row:
                    validity = True
            out = cls.check_right(board_state, col, row)
            if out:
                if out[0] == new_col and out[1] == new_row:
                    validity = True
            # Now return the answer
        return validity

    @classmethod
    def check_up(cls, board_state, col, row):
        """
        Function checks if the current move is allowed to move up one space
        or can legally jump
        :param board_state: Current state of the board
        :param col: Column number of the position of the current piece
        :param row: Row number of the position of the current piece
        :return:
        """
        # Ensure that it's not at the very top of the board, and there is at
        # least 1 space to allow it to move upwards
        if row != board_state.min_row and board_state.board[col][row - 1] == '-':
            return col, row-1
        # Check that if there is a space and it is occupied by a black or white
        # piece that there is space to allow the current piece to jump
        elif row != board_state.min_row and (
                    board_state.board[col][row - 1] == 'O' or
                    board_state.board[col][row - 1] == '@'):
            # Make sure its not on the second row of the board otherwise
            # there would be no more board left after you jumped over the piece
            if row != board_state.min_row + 1 and \
                            board_state.board[col][row - 2] == '-':
                return col, row-2
            else:
                return False
        else:
            # Otherwise the piece is not allowed to move upwards
            return False

    @classmethod
    def check_down(cls, board_state, col, row):
        """
        Function checks if the current move is allowed to move down one space
        or can legally jump
        :param board_state: Current state of the board
        :param col: Column number of the position of the current piece
        :param row: Row number of the position of the current piece
        :return:
        """
        # Ensure that it's not at the very bottom of the board, and there is at
        # least 1 space to allow it to move downwards
        if row != board_state.max_row and \
                board_state.board[col][row + 1] == '-':
            return col, row+1
        # Check that if there is a space and it is occupied by a black or white
        # piece that there is space to allow the current piece to jump
        elif row != board_state.max_row and (
                        board_state.board[col][row + 1] == 'O' or
                        board_state.board[col][row + 1] == '@'):
            # Make sure its not on the second last row of the board otherwise
            # there would be no more board left after you jumped over the piece
            if row != board_state.max_row-1 and \
                      board_state.board[col][row + 2] == '-':
                return col, row+2
            else:
                return False
        else:
            # Otherwise the piece is not allowed to move downwards
            return False

    @classmethod
    def check_left(cls, board_state, col, row):
        """
        Function checks if the current move is allowed to move left one space
        or can legally jump
        :param board_state: Current state of the board
        :param col: Column number of the position of the current piece
        :param row: Row number of the position of the current piece
        :return:
        """
        # Ensure that it's not at the very left of the board, and there is at
        # least 1 space to allow it to move left
        if col != board_state.min_col and board_state.board[col - 1][row] == '-':
            return col-1, row
        # Check that if there is a space and it is occupied by a black or white
        # piece that there is space to allow the current piece to jump
        elif col != board_state.min_col and (
                        board_state.board[col - 1][row] == 'O' or
                        board_state.board[col - 1][row] == '@'):
            # Make sure its not on the second col of the board otherwise
            # there would be no more board left after you jumped left
            if col != board_state.min_col + 1 and \
                            board_state.board[col - 2][row] == '-':
                return col-2, row
            else:
                return False
        else:
            # Otherwise the piece is not allowed to move leftwards
            return False

    @classmethod
    def check_right(cls, board_state, col, row):
        """
        Function checks if the current move is allowed to move right one space
        or can legally jump
        :param board_state: Current state of the board
        :param col: Column number of the position of the current piece
        :param row: Row number of the position of the current piece
        :return:
        """
        # Ensure that it's not at the very right of the board, and there is at
        # least 1 space to allow it to move right
        if col != board_state.max_col and \
                board_state.board[col + 1][row] == '-':
            return col+1, row
        # Check that if there is a space and it is occupied by a black or white
        # piece that there is space to allow the current piece to jump
        elif col != board_state.max_col and (
                        board_state.board[col + 1][row] == 'O' or
                        board_state.board[col + 1][row] == '@'):
            # Make sure its not on the second last col of the board otherwise
            # there would be no more board left after you jumped right
            if col != board_state.max_col-1 and \
                      board_state.board[col + 2][row] == '-':
                return col+2, row
            else:
                return False
        else:
            # Otherwise the piece is not allowed to move rightwards
            return False


def generate_moves(board_state, player='W'):
    """
    This function generates a list of all possible Moves that the player
    can make given the current board state
    :param board_state: 
    :param player: A character to identify which player to create moves for.
                   Defaults to the white player
    :return: A list of Move objects representing all valid, possible moves
    """
    poss_moves = []
    piece_locs = board_state.search_board(player)
    # For each piece, create the valid moves.
    for coord in piece_locs:
        # Checking possible up movement
        new_loc = Move.check_up(board_state, coord[0], coord[1])
        if new_loc:
            poss_moves.append(Move(board_state, coord[0], coord[1],
                                   new_loc[0], new_loc[1]))
        # Checking possible down movement
        new_loc = Move.check_down(board_state, coord[0], coord[1])
        if new_loc:
            poss_moves.append(Move(board_state, coord[0], coord[1],
                                   new_loc[0], new_loc[1]))
        # Checking possible left movement
        new_loc = Move.check_left(board_state, coord[0], coord[1])
        if new_loc:
            poss_moves.append(Move(board_state, coord[0], coord[1],
                                   new_loc[0], new_loc[1]))
        # Checking possible right movement
        new_loc = Move.check_right(board_state, coord[0], coord[1])
        if new_loc:
            poss_moves.append(Move(board_state, coord[0], coord[1],
                                   new_loc[0], new_loc[1]))

    return poss_moves


def count_pos_moves(board_state, player='W'):
    """
    This function counts the total number of legal moves available for player
    given the current board_state. This is in the movement phase of the game
    and assumes all regular moves and jumps available including ones which
    may eliminate the player's pieces
    :param board_state: A BoardState object containing the current state of
                        the game.
    :param player: A character indicating which player's legal moves to count.
                   Defaults to the White player
    :return: Integer corresponding to the number of moves currently
    """
    piece_locs = board_state.search_board(player)
    valid_count = 0

    # For each piece, count the number of valid moves
    for coord in piece_locs:
        if Move.check_up(board_state, coord[0], coord[1]):
            valid_count += 1
        if Move.check_down(board_state, coord[0], coord[1]):
            valid_count += 1
        if Move.check_left(board_state, coord[0], coord[1]):
            valid_count += 1
        if Move.check_right(board_state, coord[0], coord[1]):
            valid_count += 1
    # Return the count
    return valid_count


def is_suicide(board_state, col, row, enemy):
    """
    This function checks if a place where the white piece is moving to will
    cause it to die
    :param board_state: A BoardState object containing the current state of the
                        game.
    :param col: Destination column
    :param row: Destination row
    :param enemy: Character representing the enemies piece
    :return: True if the piece will be killed there and False otherwise
    """

    if board_state.check_horiz_elim(tuple(enemy), col, row):
        return True
    elif board_state.check_vert_elim(tuple(enemy), col, row):
        return True
    else:
        return False


def check_piece(board_state, goal_tiles, col, row, enemy):
    """
    This function checks if there are any desirable spots surrounding the piece
    used during the movement phase to direct piece movement.
    A desirable state is defined as
        - A spot that can kill an enemy piece
    :param board_state: A BoardState object
    :param goal_tiles: An existing list to add the goal tile to
    :param col: The col number of piece to check
    :param row: The row number of piece to check
    :param enemy: Character representing an enemy piece
    :return: None
    """

    # Checking vertical
    if row-1 >= board_state.min_row and row+1 <= board_state.max_row:
        # Check the top side of the piece
        if board_state.board[col][row-1] == 'X':
            # If occupied check the other side for a free space
            if board_state.board[col][row+1] != enemy:
                if not is_suicide(board_state, col, row+1, enemy):
                    goal_tiles.append((col, row+1))
        # Check the bottom side of the piece
        elif board_state.board[col][row+1] == 'X':
            # If occupied check the other side for a free space
            if board_state.board[col][row-1] != enemy:
                if not is_suicide(board_state, col, row-1, enemy):
                    goal_tiles.append((col, row-1))
        # Check if top is empty and bottom is empty
        elif board_state.board[col][row-1] != enemy and \
                board_state.board[col][row+1] != enemy:
            if not is_suicide(board_state, col, row - 1, enemy):
                goal_tiles.append((col, row-1))
            if not is_suicide(board_state, col, row + 1, enemy):
                goal_tiles.append((col, row+1))

    # Checking horizontal
    if col-1 >= board_state.min_col and col+1 <= board_state.max_col:
        # Check left side of the piece
        if board_state.board[col-1][row] == 'X':
            # If occupied check the other side for a free space
            if board_state.board[col+1][row] != enemy:
                if not is_suicide(board_state, col+1, row, enemy):
                    goal_tiles.append((col+1, row))
        # Check the right side of the piece
        elif board_state.board[col+1][row] == 'X':
            # If occupied check the other side for a free space
            if board_state.board[col-1][row] != enemy:
                if not is_suicide(board_state, col-1, row, enemy):
                    goal_tiles.append((col-1, row))
        # Check if left is empty and right is empty
        elif board_state.board[col-1][row] != enemy and \
                board_state.board[col+1][row] != enemy:
            if not is_suicide(board_state, col-1, row, enemy):
                goal_tiles.append((col-1, row))
            if not is_suicide(board_state, col+1, row, enemy):
                goal_tiles.append((col+1, row))
    return


def find_goal_tiles(board_state, piece):
    """
    This function finds where the presence of a white piece would eliminate a
    black or be on the side of a black
    :param board_state: A BoardState object containing the current state of the
                        game
    :param piece: A character that represents our player's pieces
    :return goal_tiles: A list of goal coordinates
    """

    # Get the enemy character
    if piece == 'O':
        enemy = '@'
    else:
        enemy = 'O'

    goal_tiles = []
    enemies = board_state.search_board_char(enemy)
    while len(enemies) != 0:
        curr_enemy = enemies.pop()
        col = curr_enemy[0]
        row = curr_enemy[1]
        # Check the piece
        check_piece(board_state, goal_tiles, col, row, enemy)

    # Convert into a set then back to list to remove duplicates
    return list(set(goal_tiles))


def find_goal_tiles_piece(board_state, black_col, black_row):
    """
    This function finds the goal tiles for a single piece
    :param board_state: BoardState object containing the current state of the
                        game
    :param black_col: Column number of the black piece that will be inspected
    :param black_row: Row number of the black piece that will be inspected
    :return: A list of coordinates referring to the goal tiles for that piece
    """
    goal_tiles = []
    check_piece(board_state, goal_tiles, black_col, black_row)

    return goal_tiles


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


def match_white_and_goal_tile(board_state):
    """
    This function finds the distances between a white and a goal_tile
    :param board_state: A BoardState object containing the current state of the
                        game
    :return sd_w_gt: (sorted by) Shortest distance from every white to nearest
                      goal_tile, white, goal_tile
    """
    goal_tiles = find_goal_tiles(board_state)
    whites = board_state.search_board('W')
    sd_w_gt = []
    closest_goal_tile = None

    while len(whites) != 0:
        current_white = whites.pop()
        # Set a really high distance to minimise at first
        closest_distance = 1000
        # Check which white pieces are closest to the goal tiles
        for coords in goal_tiles:
            current_distance = distance_between(coords[0], coords[1],
                                                current_white[0], current_white[1])
            if current_distance < closest_distance:
                closest_distance = current_distance
                closest_goal_tile = coords

        sd_w_gt.append((closest_distance, current_white, closest_goal_tile))
    return sorted(sd_w_gt)


def match_white_and_goal_tile_piece(board_state, black_col, black_row):
    """
    This function finds the distances between a white and the goal tiles
    for a single black piece
    :param board_state: A BoardState object containing the current state of the
                        game
    :param black_col: Column number of the black piece to look at
    :param black_row: Row number of the black piece to look at
    :return sd_w_gt: (sorted by) Shortest distance from every white to nearest
                      goal_tile, white, goal_tile
    """
    goal_tiles = find_goal_tiles_piece(board_state, black_col, black_row)
    whites = board_state.search_board('W')
    sd_w_gt = []
    closest_goal_tile = None

    while len(whites) != 0:
        current_white = whites.pop()
        # Set a really high distance to minimise at first
        closest_distance = 1000
        # Check which white pieces are closest to the goal tiles
        for coords in goal_tiles:
            current_distance = distance_between(coords[0], coords[1],
                                                current_white[0], current_white[1])
            if current_distance < closest_distance:
                closest_distance = current_distance
                closest_goal_tile = coords

        sd_w_gt.append((closest_distance, current_white, closest_goal_tile))
    return sorted(sd_w_gt)


def match_white_and_black(board_state):
    """
    This function is meant to assign the white pieces to the black pieces that
    they are closest to
    :param board_state: A BoardState object containing the current state
    :return: A list containing tuples of the form (dist, white_coord, black_coord)
    """
    blacks = board_state.search_board('B')
    whites = board_state.search_board('W')
    sd_w_gt = []
    closest_black = None
    while len(whites) != 0:
        current_white = whites.pop()
        # Set a really high distance to minimise at first
        closest_distance = 1000
        # Check which black pieces are closest to the current white piece
        for coords in blacks:
            current_distance = distance_between(coords[0], coords[1],
                                                current_white[0], current_white[1])
            if current_distance < closest_distance:
                closest_distance = current_distance
                closest_black = coords

        # Assign the information and add to the list
        sd_w_gt.append((closest_distance, current_white, closest_black))
    return sorted(sd_w_gt)


def sorted_generate_moves_piece(board_state, black_piece):
    """
    This function generates all legal, non-suicidal moves in order of distance
    from the single specified black piece
    :param board_state: A BoardState object containing the current state of the
                        game
    :param black_piece: The coordinates of the black piece to look at
    :return: A list of Move objects representing all valid, possible moves
    """
    poss_moves = []
    pieces = match_white_and_goal_tile_piece(board_state, black_piece[0], black_piece[1])
    for piece in pieces:
        distance = piece[0]
        white_pos = piece[1]
        goal_tile_pos = piece[2]

        # Checking possible up movement
        new_loc = Move.check_up(board_state, white_pos[0], white_pos[1])
        # Valid move
        if new_loc:
            # Check suicide
            if not is_suicide(board_state, new_loc[0], new_loc[1]):
                # Does it decrease distance to the closest goal_tile?
                new_dist = distance_between(new_loc[0], new_loc[1],
                                            goal_tile_pos[0], goal_tile_pos[1])
                if new_dist < distance:
                    move = Move(board_state, white_pos[0], white_pos[1],
                                new_loc[0], new_loc[1])
                    poss_moves.append(move)

        # Checking possible down movement
        new_loc = Move.check_down(board_state, white_pos[0], white_pos[1])
        # Valid move
        if new_loc:
            # Check suicide
            if not is_suicide(board_state, new_loc[0], new_loc[1]):
                # Does it decrease distance to the closest goal_tile?
                new_dist = distance_between(new_loc[0], new_loc[1],
                                            goal_tile_pos[0], goal_tile_pos[1])
                if new_dist < distance:
                    move = Move(board_state, white_pos[0], white_pos[1],
                                new_loc[0], new_loc[1])
                    poss_moves.append(move)

        # Checking possible left movement
        new_loc = Move.check_left(board_state, white_pos[0], white_pos[1])
        # Valid move
        if new_loc:
            # Check suicide
            if not is_suicide(board_state, new_loc[0], new_loc[1]):
                # Does it decrease distance to the closest goal_tile?
                new_dist = distance_between(new_loc[0], new_loc[1],
                                            goal_tile_pos[0], goal_tile_pos[1])
                if new_dist < distance:
                    move = Move(board_state, white_pos[0], white_pos[1],
                                new_loc[0], new_loc[1])
                    poss_moves.append(move)

        # Checking possible right movement
        new_loc = Move.check_right(board_state, white_pos[0], white_pos[1])
        if new_loc:
            if not is_suicide(board_state, new_loc[0], new_loc[1]):
                new_dist = distance_between(new_loc[0], new_loc[1],
                                            goal_tile_pos[0], goal_tile_pos[1])
                if new_dist < distance:
                    move = Move(board_state, white_pos[0], white_pos[1],
                                new_loc[0], new_loc[1])
                    poss_moves.append(move)

    return poss_moves


def sorted_generate_moves(board_state):
    """
    This function generates all legal, non-suicidal moves in order of distance
    from blacks
    :param board_state: A BoardState object containing the current state of the
                        game
    :param : A BoardState object holding the initial board config
    :return: A list of Move objects representing all valid, possible moves
    """
    poss_moves = []
    pieces = match_white_and_goal_tile(board_state)
    for piece in pieces:
        distance = piece[0]
        white_pos = piece[1]
        goal_tile_pos = piece[2]

        # Checking possible up movement
        new_loc = Move.check_up(board_state, white_pos[0], white_pos[1])
        # Valid move
        if new_loc:
            # Check suicide
            if not is_suicide(board_state, new_loc[0], new_loc[1]):
                # Does it decrease distance to the closest goal_tile?
                new_dist = distance_between(new_loc[0], new_loc[1],
                                            goal_tile_pos[0], goal_tile_pos[1])
                if new_dist < distance:
                    move = Move(board_state, white_pos[0], white_pos[1],
                                new_loc[0], new_loc[1])
                    poss_moves.append(move)

        # Checking possible down movement
        new_loc = Move.check_down(board_state, white_pos[0], white_pos[1])
        # Valid move
        if new_loc:
            # Check suicide
            if not is_suicide(board_state, new_loc[0], new_loc[1]):
                # Does it decrease distance to the closest goal_tile?
                new_dist = distance_between(new_loc[0], new_loc[1],
                                            goal_tile_pos[0], goal_tile_pos[1])
                if new_dist < distance:
                    move = Move(board_state, white_pos[0], white_pos[1],
                                new_loc[0], new_loc[1])
                    poss_moves.append(move)

        # Checking possible left movement
        new_loc = Move.check_left(board_state, white_pos[0], white_pos[1])
        # Valid move
        if new_loc:
            # Check suicide
            if not is_suicide(board_state, new_loc[0], new_loc[1]):
                # Does it decrease distance to the closest goal_tile?
                new_dist = distance_between(new_loc[0], new_loc[1],
                                            goal_tile_pos[0], goal_tile_pos[1])
                if new_dist < distance:
                    move = Move(board_state, white_pos[0], white_pos[1],
                                new_loc[0], new_loc[1])
                    poss_moves.append(move)

        # Checking possible right movement
        new_loc = Move.check_right(board_state, white_pos[0], white_pos[1])
        if new_loc:
            if not is_suicide(board_state, new_loc[0], new_loc[1]):
                new_dist = distance_between(new_loc[0], new_loc[1],
                                            goal_tile_pos[0], goal_tile_pos[1])
                if new_dist < distance:
                    move = Move(board_state, white_pos[0], white_pos[1],
                                new_loc[0], new_loc[1])
                    poss_moves.append(move)

    return poss_moves
