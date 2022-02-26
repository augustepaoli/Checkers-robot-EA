import os
import sys
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from Game_Interface.board import Board
from Game.game import Game
from IA.random_player import random_player
from IA.minimax_player import minimax_player
from IA.bootstrap_player import bootstrap_player

##Methodo :
##Differentes tailles de step (ensuite le step reel est egal a ce step * 1/sqrt(nombre de games))
##pour chacune on prend un bootstrap(3), on lui fait jouer 100 parties contre minimax(3)
##puis pour tester on refait 100 parties (sans entrainement) et on regarde le pourcentage de reussite 

steps =  [1e-4,2e-4,3e-4,4e-4,5e-4,6e-4,7e-4,8e-4,9e-4,1e-3,2e-3,3e-3,4e-3,5e-3,6e-3,7e-3,8e-3,9e-3,1e-2,2e-2,3e-2,4e-2,5e-2,6e-2,7e-2,8e-2,9e-2,1e-1,2e-1,3e-1,4e-1,5e-1,6e-1,7e-1,8e-1,9e-1,1e0]
results=[]
k=0
for step in steps :

    boot=bootstrap_player(2)
    boot.step=step
    boot.theta=np.array([-1.0,1.0,-1.0,1.0])
    
    p2=minimax_player(2)
    for i in range(100) :
        game=Game(boot,p2)
        game.end_game(verbose=False,ignore_history=False)

    boot.set_learning(False)
    boot.counting_error=True

    p2=minimax_player(2)
    for i in range(20) :
        game=Game(boot,p2)
        game.end_game(verbose=False,ignore_history=False)

    print("step : " + str(step))
    print(boot.total_square_error)
    results.append(boot.total_square_error)

plt.plot(steps,results)
plt.xscale('log')
plt.title("Accuracy of the score prediction \n depending on the step used for the GD")
plt.xlabel('Step')
plt.ylabel("Mean of the squared error")
plt.legend()
plt.show()
