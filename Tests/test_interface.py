import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from Game.game_vs_IA import Game_vs_IA
from IA.minimax_player import minimax_player

p=minimax_player(2)
game = Game_vs_IA(p)
game.end_game(ignore_history=False)