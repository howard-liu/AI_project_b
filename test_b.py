###
# File that is used to test different aspects of the Part B implementation of
# the AI project
###

from action import *
from board_state import *
from player import *
import enemy_player as ep
from placing_strategy import *
from moving_strategy import *

player = Player('white')
enemy_player = ep.Player('black')
board = BoardState()

# # Movement Phase
# for i in range(12):
#     player_action = Action(board, '@', player.action(i))
#     board.modify(player_action, '@')
#     enemy_player.update(player_action.return_action())
#     # print(board)
#
#     enemy_action = Action(board, 'O', enemy_player.action(i))
#     board.modify(enemy_action, 'O')
#     player.update(enemy_action.return_action())
#     # print(board)
#
# print(board)
#
# for i in range(256):
#     player_action = Action(board, '@', player.action(i))
#     board.modify(player_action, '@')
#     enemy_player.update(player_action.return_action())
#     print(board)
#     print("Remaining blacks = " + str(len(board.search_board('B'))))
#
#     enemy_action = Action(board, 'O', enemy_player.action(i))
#     board.modify(enemy_action, 'O')
#     player.update(enemy_action.return_action())
#     print(board)
#     print("Remaining whites = " + str(len(board.search_board('W'))))


# print(Action(board, '@', action=(4, 4)))

board.modify(Action(board, action=(7, 1), enemy='@'), '@')
print(board)
board.modify(Action(board, action=(7, 3), enemy='@'), '@')
board.modify(Action(board, action=(7, 2), enemy='O'), 'O')
print(board)

# action = (6, 5), (6, 6)
# a = Action(board_state=board, action=action, enemy='@')
# board.modify(a, '@')
# print(board)
# print(count_pos_moves(board))

