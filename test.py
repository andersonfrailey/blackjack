from blackjack import *
from time import time

start = time()
new_game = Game()
new_game.sim_game(8, 6, 100000)
print time() - start
