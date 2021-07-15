from player import *
from game import Game

game = Game(game_count=200)

game.add_player(TitForTat())
game.add_player(TitFor2Tat())
game.add_player(AllC())
game.add_player(AllD())
game.add_player(FriedMan())
game.add_player(Joss())
game.add_player(Detective())
game.add_player(Pavlov())

game.run1()
# game.run2()
players = game.return_score_board()

i = 1
for k, v in players:
    print(str(i) + "위 : " + v.name + " 점수: " + str(v.score))
    i += 1
