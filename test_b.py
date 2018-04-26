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

# Placing Phase
for i in range(12):
    player_action = Action(board, '@', player.action(i))
    board.modify(player_action, '@')
    enemy_player.update(player_action.return_action())
    # print(board)

    enemy_action = Action(board, 'O', enemy_player.action(i))
    board.modify(enemy_action, 'O')
    player.update(enemy_action.return_action())
    # print(board)



# print("(Update) White player: \n" + str(player.board))
# print("(Update) Black player: \n" + str(enemy_player.board))


# print(board)
#
i = 0
current, opponent = player, enemy_player

while i < 256:
    player_action = Action(board, current.enemy, current.action(i))
    print("Player plays move: " + str(player_action.return_action()))
    print("(Update) Current player: \n" + str(current.board))
    board.modify(player_action, current.enemy)
    print(board)
    opponent.update(player_action.return_action())
    print("(Update) Opponent player: \n" + str(opponent.board))

    print(current.board == opponent.board)
    print(current.board == board)
    print()
    current, opponent = opponent, current
    i += 1

    # print(board)
    # print("Remaining blacks = " + str(len(board.search_board('B'))))

    # enemy_action = Action(board, 'O', enemy_player.action(i))
    # board.modify(enemy_action, 'O')
    # player.update(enemy_action.return_action())
    # print(board)
    # print("Remaining whites = " + str(len(board.search_board('W'))))




# print(Action(board, '@', action=(4, 4)))

# board.modify(Action(board, action=(5, 2), enemy='O'), 'O')
# print(board)
# board.modify(Action(board, action=(4, 3), enemy='@'), '@')
# print(board)
# board.modify(Action(board, action=(5, 4), enemy='O'), 'O')
# print(board)
# board.modify(Action(board, action=((5, 1)), enemy='@'), '@')
# print(board)
# board.modify(Action(board, action=((4, 3), (5, 3)), enemy='@'), '@')
# print(board)

# action = (6, 5), (6, 6)
# a = Action(board_state=board, action=action, enemy='@')
# board.modify(a, '@')
# print(board)
# print(count_pos_moves(board))

