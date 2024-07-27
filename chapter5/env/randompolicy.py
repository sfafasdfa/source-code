import numpy as np
from mcsrlenv import raw_env
import os
import random
import csv
def getaction(pt,size):
    actiondict ={}
    if pt[0] == 0:
        actiondict[2] = 0
    else:
        actiondict[2] = 1
    if pt[0] == size-1:
        actiondict[3] = 0
    else:
        actiondict[3] = 1
    if pt[1] == 0:
        actiondict[0] = 0
    else:
        actiondict[0] = 1
    if pt[1] == size-1:
        actiondict[1] = 0
    else:
        actiondict[1] = 1
    randnum =random.random()
    if randnum < (actiondict[0])/(actiondict[0]+actiondict[1]+actiondict[2]+actiondict[3]):
        return 0
    elif randnum < (actiondict[0]+actiondict[1])/(actiondict[0]+actiondict[1]+actiondict[2]+actiondict[3]):
        return 1
    elif randnum < (actiondict[0]+actiondict[1]+actiondict[2])/(actiondict[0]+actiondict[1]+actiondict[2]+actiondict[3]):
        return 2
    else:
        return 3
if __name__ == '__main__':
    env = raw_env()
    episodelimit = 1000
    datalist = []
    env.reset()
    traclist = []
    for i in range(episodelimit):
        print("=========episode"+str(i))
        traclist = []
        env.reset()
        workers = env.agents_coord
        points = env.points_coord
        actions = {}
        epi_total_rwd = 0
        for j in range(100):
            time = j
            cx = env.agents_coord[env.agents[0]][0]
            cy = env.agents_coord[env.agents[0]][1]
            traclist.append({'time':time,'x':cx,'y':cy})
            for worker in workers:
                act = getaction(workers[worker],env.SIZE)
                actions[worker] = act
            obs, rwd, ter, tru, inf = env.step(actions=actions)
            for worker in workers:
                workers[worker] = env.agents_coord[worker]
                epi_total_rwd += rwd[worker]
        print(epi_total_rwd)
        #updatemap
        datalist.append({'episode':i,'total_reward':epi_total_rwd})
    # print(datalist[999])
    # with open('randompolicy.csv', 'w') as file:
    #     header = ['episode','total_reward']
    #     # Create a CSV dictionary writer and add the student header as field names
    #     writer = csv.DictWriter(file, fieldnames=header)
    #     # Use writerows() not writerow()
    #     writer.writeheader()
    #     writer.writerows(datalist)
    with open('randomtrac.csv',"w") as file:
        header = ['time','x','y']
        writer = csv.DictWriter(file,fieldnames=header)
        writer.writeheader()
        writer.writerows(traclist)
    print(env.count)