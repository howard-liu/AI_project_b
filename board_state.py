###
# Module containing data structures and appropriate support functions that are
# used by the Project to implement an AI that can play the
# "Watch your back!" board game.
# Structures implemented by Edmond Pan (841389)
###


class NoBoardReadError(Exception):
    """
    Basic exception class to create an error whenever a board state is
    created without being read from input or copying from an existing state
    """
    pass


class BoardState:

    def __init__(self, ins_type='N', other_state=None):
        """
        Constructor to initialise and fill in the current board state
        :param ins_type: Character determining which method to use to insert the
                         position of pieces into the board structure. If the
                         character is 'I' then insert from stdin or
                         insertion is done by reading from an existing
                         BoardState object and then doing the appropriate
                         movement of the piece. Otherwise create an empty
                         board representation to fill with more data specified
                         by 'N'. Default insertion is specified by 'N'
        :param other_state: Another BoardState object to copy the board from
        """

        # Variable storing number of shrinks that has occurred
        self.n_shrinks = 0

        # Variables storing the current range of cols and rows that allow pieces
        # to be legally placed on
        self.min_col = 0
        self.max_col = 7
        self.min_row = 0
        self.max_row = 7


        # Coordinate access is of the format self.board[col][row]. Initialise
        # all values to empty spaces denoted by "-" as well as adding in the
        # initial corner squares.
        self.board = [['-' for j in range(self.max_row + 1)]
                      for i in range(self.max_col + 1)]
        for coord in [(0, 0), (7, 0), (7, 7), (0, 7)]:
            col, row = coord
            self.board[col][row] = 'X'

        # If ins_type is 'N' then do nothing and just assign the empty board
        if ins_type == 'N':
            pass
        # If ins_type is 'I' then read from input
        elif ins_type == 'I':
            self.__read_input__()
        elif isinstance(other_state, BoardState):
            # Takes an board_state object and copies its contents into the
            # board structure
            for i in range(len(other_state.board)):
                for j in range(len(other_state.board[i])):
                    self.board[j][i] = other_state.output_piece(j, i)
        else:
            raise NoBoardReadError('Data is not in correct format. Please'
                                   ' check the inputs')
        # Make sure any pieces that should be eliminated are eliminated
        self.static_eliminate_piece()

    def __read_input__(self):
        """
        Function that reads an input file from the standard input into the
        board data structure.
        :return:
        """
        for i in range(self.max_row + 1):
            # Read in one line
            line = input()
            # Split it based on whitespace
            line = line.split()
            # For each line add it to the correct row and column in table
            j = 0
            for piece in line:
                self.board[j][i] = piece
                j += 1

    def __str__(self):
        """
        To string function that prints out what the board looks like
        :return: None
        """
        # Add the numbers as a header
        line = '  0 1 2 3 4 5 6 7 \n'
        for i in range(len(self.board)):
            # Add the current row number to the beginning
            line += str(i) + ' '
            for j in range(len(self.board[i])):
                # Swap coords since access is done by (col, row) not (row, col)
                # then add to the current line
                line += self.board[j][i] + ' '
            # Add newline character to end the current line and start the next
            line += '\n'
        return line

    def __lt__(self, other):
        """
        Function to return if a board state is less than another one. It is
        considered less than if there are less black pieces than white pieces
        self < other
        :param other:
        :return:
        """
        if isinstance(other, BoardState):
            num_whites = len(self.search_board('W'))
            num_blacks = len(self.search_board('B'))
            return num_blacks < num_whites

        else:
            return False

    def __eq__(self, other):
        """
        Function to test if the current board state is equal to another one
        :param other: The other object to check against
        :return: True if they are the same and False otherwise
        """
        if self is other:
            return True
        elif type(self) != type(other):
            return False
        else:
            # Compare if the pieces on the board are in the same positions
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[j][i] != other.board[j][i]:
                        print("Difference found at {}".format(str((j, i))))
                        return False
            # Otherwise they must be the same state
            return True

    def __hash__(self):
        """
        Makes a BoardState object hashable
        :return: An integer
        """
        return hash(str(self))

    def search_board(self, player='W'):
        """
        This function searches the board for the specified player's pieces.
        :param player: A character indicating which player's pieces to check.
                       Defaults to 'W' i.e. the white player
        :return: A list of tuples containing the coords (col, row) of the
                 player's pieces
        """
        output = []
        if player == 'W':
            # If white player search for 'O' characters on the board
            piece_char = 'O'
        else:
            # Must be searching for black player's pieces which are '@' chars
            piece_char = '@'

        # Looping across the legal area of the board and then adding the found
        # pieces to the output
        for i in range(self.min_row, self.max_row + 1):
            for j in range(self.min_col, self.max_col + 1):
                if self.board[j][i] == piece_char:
                    output.append((j, i))

        return output

    def output_piece(self, j, i):
        """
        This function outputs the character given the coordinates
        :param j: Coordinates
        :param i: Coordinates
        :return: A char representing the piece of the board
            at the coordinates
        """
        return self.board[j][i]

    def modify(self, action, enemy):
        """
        This function modifies the board depending on whether move is a place
        type or move type.
        :param action: The Action object
        :param enemy: A character representing the enemy pieces
        :return: None
        """
        # Select our piece
        if enemy == '@':
            piece = 'O'
        else:
            piece = '@'
        # Choose the correct movement method\
        if action is None:
            # Do nothing to the board if the movement is a forfeited one
            return
        elif action.move_type == 'place':
            self.__place_piece__(action.move, piece)
            self.eliminate_piece(action.move.curr_col, action.move.curr_row)
        elif action.move_type == 'move':
            # The move must have been a movement one.
            self.__move_piece__(action.move)
            self.eliminate_piece(action.move.new_col, action.move.new_row)

    def shrink_board(self):
        """
        When called this method will shrink the board and eliminate any pieces
        that are no longer in a legal position.
        IMPORTANT NOTE: COPIES MOST CODE FROM THE SHRINK BOARD METHOD included
        in referee.py written by Matt Farrugia and Shreyash Patodia
        :return: None
        """
        # Number of shrinks that has currently take place for this current state
        s = self.n_shrinks

        # Now remove the spots on the outer edge of the board
        for i in range(s, 8 - s):
            for square in [(i, s), (s, i), (i, 7-s), (7-s, i)]:
                row, col = square
                self.board[col][row] = ' '

        # Increment the number of shrinks that has occurred. Also modify the
        # variables storing the legal area of the board now
        self.n_shrinks = s = s + 1
        self.min_col += 1
        self.max_col -= 1
        self.min_row += 1
        self.max_row -= 1

        # Add the new corners and eliminate the pieces around corners
        for corner in [(s, s), (s, 7-s), (7-s, 7-s), (7-s, s)]:
            col, row = corner
            self.board[col][row] = 'X'
            self.eliminate_piece(col, row)

    def __place_piece__(self, move, piece):
        """
        This function adds a piece to the board during the placing phase.
        :param move: A Move object containing the placement location
        :param piece: A character representing the player or enemies piece to be
                      added.
        :return: None
        """
        self.board[move.curr_col][move.curr_row] = piece
        return

    def __move_piece__(self, move):
        """
        This function acts out the move on the board state
        :param move: Move object describing moving a piece
        :return: None
        """

        # Read the characters from move
        curr_char = self.board[move.curr_col][move.curr_row]
        new_char = self.board[move.new_col][move.new_row]

        # Swap these characters
        self.board[move.curr_col][move.curr_row] = new_char
        self.board[move.new_col][move.new_row] = curr_char

        return

    def check_horiz_elim(self, enemy, col, row):
        """
        Function that checks for horizontal eliminations.
        :param enemy: A tuple of character(s) corresponding to the enemy's piece
                      on the board. i.e. 'O' for white and '@' for black
        :param col: Column number of piece to check
        :param row: Row number of piece to check
        :return: Returns true if the piece being checked will be destroyed and
                 False otherwise
        """
        # Only check left and right if the piece is not at the very edge
        # of the board
        if self.min_col < col < self.max_col:
            # Check if both right and left sides are blocked by a corner or
            # a enemy piece
            if self.board[col + 1][row] in enemy and \
                            self.board[col - 1][row] in enemy:
                # Then the piece gets destroyed
                return True
            elif self.board[col + 1][row] in enemy and \
                    self.board[col - 1][row] == 'X':
                return True
            elif self.board[col + 1][row] == 'X' and \
                    self.board[col - 1][row] in enemy:
                return True
        else:
            # If the piece is at the very left or right of the board it is not
            # possible to eliminate it horizontally
            return False

    def check_vert_elim(self, enemy, col, row):
        """
        Function that checks for vertical eliminations.
        :param enemy: A tuple of character(s) corresponding to the enemy's piece
                      on the board. i.e. 'O' for white and '@' for black
        :param col: Column number of piece to check
        :param row: Row number of piece to check
        :return: Returns true if the piece being checked will be destroyed and
                 False otherwise
        """
        # Only check up and down if the piece is not at the very edge
        # of the board
        if self.min_row < row < self.max_row:
            # Check if both up and down sides are blocked by a corner or a
            # enemy piece
            if self.board[col][row + 1] in enemy and \
               self.board[col][row - 1] in enemy:
                # Then the piece gets destroyed
                return True
            elif self.board[col][row + 1] in enemy and \
                    self.board[col][row - 1] == 'X':
                return True
            elif self.board[col][row + 1] == 'X' and \
                    self.board[col][row - 1] in enemy:
                return True
        else:
            # If the piece is at the very top or very bottom of the board,
            # it is not possible to eliminate it vertically.
            return False

    def __surround_elim__(self, col, row):
        """
        This function eliminates the piece at col, row if it has been surrounded
        by an enemy piece or is blocked in by an enemy piece at a corner of the
        board
        :param col: Col value of the piece to check if the enemy has surrounded
                    it
        :param row: Row value of the piece to check if the enemy has surrounded
                    it
        :param enemy: A character representing the enemy piece
        :return: None
        """
        enemy = self.__get_enemies__(self.board[col][row])
        # Check for both horizontal and vertical elimination
        if self.check_horiz_elim(enemy, col, row):
            self.board[col][row] = '-'
        elif self.check_vert_elim(enemy, col, row):
            self.board[col][row] = '-'

        return None

    @classmethod
    def __get_enemies__(cls, piece):
        """
        This function returns a set containing the characters which represent
        the enemies of the input piece
        :param piece: A character representing a player's piece
        :return: A set of characters representing the enemy pieces
        """
        if piece == '@':
            return {'O', 'X'}
        elif piece == 'O':
            return {'@', 'X'}
        else:
            return set()

    def eliminate_piece(self, col, row):
        """
        Checks if the piece at col, row can eliminate any other pieces and once
        those are eliminated proceeds to check if the piece itself will be
        eliminated by the surrounding enemy pieces
        :param col: Col value of piece to check if it eliminates any enemies or
                    if it is eliminated by the enemy
        :param row: Row value of piece to check if it eliminates any enemies or
                    if it is eliminated by the enemy
        :param enemy: A character representing the enemy piece
        :return: None
        """
        # Get the target of the current piece
        piece = self.board[col][row]
        if piece == '@':
            target = tuple('O')
        elif piece == 'O':
            target = tuple('@')
        else:
            # It is a corner
            target = ('@', 'O')

        # List that stores the different adjacent squares to check enemy pieces
        # for elimination.
        # In order, [left_square, right_square, down_square, up_square]
        adj_squares = [(col-1, row), (col+1, row), (col, row+1), (col, row-1)]

        for target_col, target_row in adj_squares:
            # Check coords are valid
            if self.min_col <= target_col <= self.max_col and \
               self.min_row <= target_row <= self.max_col:
                if self.board[target_col][target_row] in target:
                    # From the enemy pieces perspective, so see if our pieces
                    # can eliminate it
                    self.__surround_elim__(target_col, target_row)

        # Now check if this piece can still be eliminated by the surrounding
        # pieces
        self.__surround_elim__(col, row)

        return None

    def static_eliminate_piece(self):
        """
        This function ITERATIVELY checks if a board state eliminates any pieces
        and removes eliminated pieces appropriately. IT WILL NOT WORK CORRECTLY
        FOR A REAL TIME GAME OF WATCH YOUR BACK! as it does not account for the
        order in which the pieces are placed. The elimination order is biased
        towards black piece being eliminated first
        :return: None
        """
        # For all white pieces, then black pieces
        whites = self.search_board('W')
        blacks = self.search_board('B')

        # For black pieces
        while len(blacks) != 0:
            black_coord = blacks.pop()
            col = black_coord[0]
            row = black_coord[1]

            # Remove black pieces that can be eliminated
            if self.check_horiz_elim('O', col, row):
                self.board[col][row] = '-'
            elif self.check_vert_elim('O', col, row):
                self.board[col][row] = '-'

        # For white pieces
        while len(whites) != 0:
            white_coord = whites.pop()
            col = white_coord[0]
            row = white_coord[1]

            # Remove whites pieces that can be eliminated
            if self.check_horiz_elim('@', col, row):
                self.board[col][row] = '-'
            elif self.check_vert_elim('@', col, row):
                self.board[col][row] = '-'

        return
