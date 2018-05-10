###
# This Python class contains a tree object used to store board states to allow
# a traversal by different algorithms
###

from watch_your_back import *


class BoardTree:
    """
    This class represents a tree containing all of the board states with
    specified depth and branching factor limitations during the movement phase
    for a game of Watch your Back!
    """
    def __init__(self, initial_state, depth=2, breadth=2):
        """
        This function creates a tree to be searched using Minimax and other
        such adversarial search functions
        :param initial_state: The initial game state
        :param depth: The depth to search to
        :param breadth: The limit for the number of children for each node
        """
        game = WatchYourBack(initial_state)

        # The root node of the tree
        self.root = Node(initial_state)

        # These are the leaf nodes of our depth limited exploration to
        # run an evaluation function on
        self.leafs = []

        # Perform a depth limited exploration
        frontier = Stack(self.root)
        explored = set()
        while frontier.size() != 0:
            node = frontier.pop()
            # print(node)  # For visualisation only
            # print(node.depth)
            # print('---------NEW----------')
            if game.terminal_test(node.game_state):
                # If a terminal state is reached, can't expand further
                # so continue onto its sibling
                self.leafs.append(node)
            elif node.depth == depth:
                # Don't expand and get the next node from the Stack
                self.leafs.append(node)
            else:
                # Add the node to explored set
                explored.add(node.game_state.board_state)
                # Check if the child node has already been explored or if it
                # already exists as a frontier node. Prevents infinite cycling
                children = []
                for child in node.expand(game, breadth):
                    if child.game_state.board_state not in explored:
                        if not frontier.exists(child):
                            children.append(child)
                frontier.extend(children)


class Node:
    # IMPORTANT NOTE: This class has been adapted from the classes provided
    # by the AIMA textbook
    """
    Class defines a single node in the search tree.
    """
    def __init__(self, game_state, parent=None, move=None):
        """
        Creates a search tree Node, derived from a parent by an action.
        :param board_state: current state this node represents
        :param parent: A pointer to the parent node
        :param move: The action that was taken to get to this current state
                     stored by the node
        """
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.children = []
        self.depth = 0
        if parent:
            # If a parent node exists increase the current depth by 1
            self.depth = parent.depth + 1

    def __lt__(self, node):
        # Function taken directly from AIMA class
        return self.game_state < node.game_state

    def __str__(self):
        """
        This function defines how to represent a node as a string
        :return: A string
        """
        line = ''
        line += self.game_state.board_state.__str__()
        line += self.move.__str__()
        line += '\n'
        return line

    def child_node(self, game, move):
        """
        Creates a new child node to connect to this node
        :param game: WatchYourBack game object containing the information for
                     the rules of the game during the movement phase
        :param move: A Move object representing the move that will be performed
        :return: A Node object containing the newly created child node
        """
        # Generate the next node
        next_node = game.result(self.game_state, move)
        # Return a newly created child node with the current node set as its
        # parent
        return Node(next_node, self, move)

    def expand(self, game, child_limit):
        """
        This function lists all the other nodes that are connected to this one
        :param game: WatchYourBack game object containing the information for
                     the rules of the game during the movement phase
        :return: A list of Node objects that are reachable
        """
        # List comprehension that generates a child node for every possible
        # action in the current state
        self.children = [self.child_node(game, move)
                         for move in game.actions(self.game_state)][0:child_limit]
        return self.children

    def solution(self):
        """
        Return the sequence of actions to go from the root to this node.
        """
        return [node.move for node in self.path()[1:]]

    def path(self):
        """
        Return a list of nodes forming the path from the root to this node.
        """
        node, return_path = self, []
        while node:
            # Add the nodes in reverse order to a list until you reach the
            # root parent node which will terminate the loop
            return_path.append(node)
            node = node.parent
        # Reverse the list to get the proper path back
        return list(reversed(return_path))

    # For our problem we treat 2 nodes as equal if and only if there states
    # are equal

    def __eq__(self, other):
        """
        Function to test if the current node is equal to another one
        :param other: The other object to check against
        :return: True if they are the same and False otherwise
        """
        if self is other:
            return True
        elif type(self) != type(other):
            return False
        else:
            # A node is considered equal if it has the exact same state as
            # another node
            if self.game_state.board_state == other.game_state.board_state:
                return True
            else:
                return False

    def __hash__(self):
        return hash(self.game_state.board_state)


class Stack:
    """
    Class that implements a queue using LIFO ordering. To be used for all
    depth first search implementations
    """
    def __init__(self, data=None):
        # The basic structure is a Python list as it dynamically resizes itself
        # Also adds in a single data item if given
        self.__stack = list()
        if data:
            self.__stack.append(data)

    def extend(self, data_list):
        """
        This function iteratively adds all the elements in a list to the end
        of the stack
        :param data_list: A list of data to add to the stack
        :return: None
        """
        self.__stack.extend(data_list)

    def push(self, data):
        """
        This function adds an element to the stack
        :param data: Any bit of data to be added. For our problem this would be
                     a Node object
        :return: None
        """
        self.__stack.append(data)

    def pop(self):
        """
        Function to return the last item added into the stack
        :return: The item that was last added to the stack
        """
        # Making sure that the stack is not empty
        if len(self.__stack) > 0:
            return self.__stack.pop()
        else:
            print("ERROR: Stack is empty!!")
            return

    def size(self):
        """
        Function to return the number of items currently stored in the stack
        :return: An integer corresponding to the number of items in the stack
        """
        return len(self.__stack)

    def exists(self, data):
        """
        Function that checks if data already exists in the stack
        :param data: Any object to check for existence
        :return: True if it exists and False otherwise
        """
        return data in self.__stack
