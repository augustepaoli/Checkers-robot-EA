import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import os

import sys
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

boot1=bootstrap_player.load("trained_full_features")
boot2=bootstrap_player.load("trained_full_features_with_depth_4")
boot1.default_depth=2
boot2.default_depth=2
mini3=minimax_player(2)
mini4=minimax_player(3)

count_tot=[]
time_tot=[]

p2=random_player()
counting=[0,0,0,0]
times=[]
print("random")
for i in range(20) :
    print(i)

    start=time.time()
    game=Game(mini3,p2)
    result=game.end_game(ignore_history=False)
    t1=time.time()-start
    if result==1 :
        counting[0]+=1

    start=time.time()
    game=Game(mini4,p2)
    result=game.end_game(ignore_history=False)
    t2=time.time()-start
    if result==1 :
        counting[1]+=1

    start=time.time()
    game=Game(boot1,p2)
    result=game.end_game(ignore_history=False)
    t3=time.time()-start
    if result==1 :
        counting[2]+=1
    
    start=time.time()
    game=Game(boot2,p2)
    result=game.end_game(ignore_history=False)
    t4=time.time()-start
    if result==1 :
        counting[3]+=1
    
    times.append([t1,t2,t3,t4])

time_tot.append(np.mean(np.array(times),axis=0))
count_tot.append(np.array(counting)/len(times))
print("")

p2=minimax_player(1)
counting=[0,0,0,0]
times=[]
print("depth1")
for i in range(20) :
    print(i)

    start=time.time()
    game=Game(mini3,p2)
    result=game.end_game(ignore_history=False)
    t1=time.time()-start
    if result==1 :
        counting[0]+=1

    start=time.time()
    game=Game(mini4,p2)
    result=game.end_game(ignore_history=False)
    t2=time.time()-start
    if result==1 :
        counting[1]+=1

    start=time.time()
    game=Game(boot1,p2)
    result=game.end_game(ignore_history=False)
    t3=time.time()-start
    if result==1 :
        counting[2]+=1
    
    start=time.time()
    game=Game(boot2,p2)
    result=game.end_game(ignore_history=False)
    t4=time.time()-start
    if result==1 :
        counting[3]+=1
    
    times.append([t1,t2,t3,t4])

time_tot.append(np.mean(np.array(times),axis=0))
count_tot.append(np.array(counting)/len(times))
print("")

p2=minimax_player(2)
counting=[0,0,0,0]
times=[]
print("depth2")
for i in range(20) :
    print(i)

    start=time.time()
    game=Game(mini3,p2)
    result=game.end_game(ignore_history=False)
    t1=time.time()-start
    if result==1 :
        counting[0]+=1

    start=time.time()
    game=Game(mini4,p2)
    result=game.end_game(ignore_history=False)
    t2=time.time()-start
    if result==1 :
        counting[1]+=1

    start=time.time()
    game=Game(boot1,p2)
    result=game.end_game(ignore_history=False)
    t3=time.time()-start
    if result==1 :
        counting[2]+=1
    
    start=time.time()
    game=Game(boot2,p2)
    result=game.end_game(ignore_history=False)
    t4=time.time()-start
    if result==1 :
        counting[3]+=1
    
    times.append([t1,t2,t3,t4])

time_tot.append(np.mean(np.array(times),axis=0))
count_tot.append(np.array(counting)/len(times))
print("")

p2=minimax_player(3)
counting=[0,0,0,0]
times=[]
print("depth3")
for i in range(20) :
    print(i)

    start=time.time()
    game=Game(mini3,p2)
    result=game.end_game(ignore_history=False)
    t1=time.time()-start
    if result==1 :
        counting[0]+=1

    start=time.time()
    game=Game(p2,mini4)
    result=game.end_game(ignore_history=False)
    t2=time.time()-start
    if result==1 :
        counting[1]+=1

    start=time.time()
    game=Game(boot1,p2)
    result=game.end_game(ignore_history=False)
    t3=time.time()-start
    if result==1 :
        counting[2]+=1
    
    start=time.time()
    game=Game(boot2,p2)
    result=game.end_game(ignore_history=False)
    t4=time.time()-start
    if result==1 :
        counting[3]+=1
    
    times.append([t1,t2,t3,t4])

time_tot.append(np.mean(np.array(times),axis=0))
count_tot.append(np.array(counting)/len(times))
print("")

p2=minimax_player(4)
counting=[0,0,0,0]
times=[]
print("depth4")
for i in range(20) :
    print(i)

    start=time.time()
    game=Game(mini3,p2)
    result=game.end_game(ignore_history=False)
    t1=time.time()-start
    if result==1 :
        counting[0]+=1

    start=time.time()
    game=Game(mini4,p2)
    result=game.end_game(ignore_history=False)
    t2=time.time()-start
    if result==1 :
        counting[1]+=1

    start=time.time()
    game=Game(boot1,p2)
    result=game.end_game(ignore_history=False)
    t3=time.time()-start
    if result==1 :
        counting[2]+=1
    
    start=time.time()
    game=Game(boot2,p2)
    result=game.end_game(ignore_history=False)
    t4=time.time()-start
    if result==1 :
        counting[3]+=1
    
    times.append([t1,t2,t3,t4])

time_tot.append(np.mean(np.array(times),axis=0))
count_tot.append(np.array(counting)/len(times))
print("")

# p2=minimax_player(5)
# counting=[0,0,0,0]
# times=[]
# print("depth5")
# for i in range(20) :
#     print(i)

#     start=time.time()
#     game=Game(mini3,p2)
#     result=game.end_game(ignore_history=False)
#     t1=time.time()-start
#     if result==2 :
#         counting[0]+=1

#     start=time.time()
#     game=Game(mini4,p2)
#     result=game.end_game(ignore_history=False)
#     t2=time.time()-start
#     if result==2 :
#         counting[1]+=1

#     start=time.time()
#     game=Game(p2,boot1)
#     result=game.end_game(ignore_history=False)
#     t3=time.time()-start
#     if result==2 :
#         counting[2]+=1
    
#     start=time.time()
#     game=Game(p2,boot2)
#     result=game.end_game(ignore_history=False)
#     t4=time.time()-start
#     if result==2 :
#         counting[3]+=1
    
#     times.append([t1,t2,t3,t4])

# time_tot.append(np.mean(np.array(times),axis=0))
# count_tot.append(np.array(counting)/len(times))
# print("")  
# 
count_tot=np.array(count_tot)
time_tot=np.array(time_tot)

plt.plot(np.arange(5), count_tot[:,0], label='minimax_depth2_player')
plt.plot(np.arange(5), count_tot[:,1], label='minimax_depth3_player')
plt.plot(np.arange(5), count_tot[:,2], label='uncomplete_bootstrap_depth2_player')
plt.plot(np.arange(5), count_tot[:,3], label='complete_boostrap_depth2_player')
plt.xlabel("Depth of the opponent")
plt.ylabel("Winning rate out of 20 games")
plt.legend()
plt.title('Efficiency of the different AIs')
plt.show()

plt.plot(np.arange(5), time_tot[:,0], label='minimax_depth2_player')
plt.plot(np.arange(5), time_tot[:,1], label='minimax_depth3_player')
plt.plot(np.arange(5), time_tot[:,2], label='uncomplete_bootstrap_depth2_player')
plt.plot(np.arange(5), time_tot[:,3], label='complete_boostrap_depth2_player')
plt.xlabel("Depth of the opponent")
plt.ylabel("Mean duration of one game")
plt.legend()
plt.title('Quickness of the different AIs')
plt.show()