import numpy as np
from mcsrlenv import raw_env
import os
import random
import csv

def getactionwithrandom(pt,size):
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
def getactionwithmap(pt,size,infomap):
    actiondict ={}
    if pt[0] == 0:
        actiondict[2] = 0
    else:
        actiondict[2] = infomap[pt[0]-1][pt[1]]
    if pt[0] == size-1:
        actiondict[3] = 0
    else:
        actiondict[3] = infomap[pt[0]+1][pt[1]]
    if pt[1] == 0:
        actiondict[0] = 0
    else:
        actiondict[0] = infomap[pt[0]][pt[1]-1]
    if pt[1] == size-1:
        actiondict[1] = 0
    else:
        actiondict[1] = infomap[pt[0]][pt[1]+1]
    randnum =random.random()
    if randnum < (actiondict[0])/(actiondict[0]+actiondict[1]+actiondict[2]+actiondict[3]):
        return 0
    elif randnum < (actiondict[0]+actiondict[1])/(actiondict[0]+actiondict[1]+actiondict[2]+actiondict[3]):
        return 1
    elif randnum < (actiondict[0]+actiondict[1]+actiondict[2])/(actiondict[0]+actiondict[1]+actiondict[2]+actiondict[3]):
        return 2
    else:
        return 3
def updatemap(infomap,trajectset,size,wk_total_rwd):
    newmap = infomap
    valuemap = np.zeros((size,size))
    for wk in trajectset:
        count = len(trajectset[wk])
        value = wk_total_rwd[wk]/count
        for pt in trajectset[wk]:
            valuemap[pt[0]][pt[1]] += value
    for i in range(size):
        for j in range(size):
            newmap[i][j] = 0.9*newmap[i][j]+valuemap[i][j]
    return newmap
if __name__ == '__main__':
    env = raw_env()
    episodelimit = 1000
    datalist = []
    env.reset()
    infomap = 25*np.ones((env.SIZE,env.SIZE))
    traclist = []
    for i in range(episodelimit):
        print("=========episode"+str(i))
        traclist = []
        env.reset()
        workers = env.agents_coord
        points = env.points_coord
        actions = {}
        epi_total_rwd = 0
        trajectset = {}
        wk_total_rwd = {}
        for worker in workers:
            trajectset[worker] = set()
            coord = (workers[worker][0],workers[worker][1])
            trajectset[worker].add(coord)
            wk_total_rwd[worker] = 0
        for j in range(100):
            time = j
            cx = env.agents_coord[env.agents[0]][0]
            cy = env.agents_coord[env.agents[0]][1]
            traclist.append({'time':time,'x':cx,'y':cy})
            for worker in workers:
                randnum = random.random()
                if randnum > (0.9-i/(episodelimit)):
                    act = getactionwithmap(workers[worker],env.SIZE,infomap)
                else:
                    act = getactionwithrandom(workers[worker],env.SIZE)
                actions[worker] = act
            obs, rwd, ter, tru, inf = env.step(actions=actions)
            for worker in workers:
                workers[worker] = env.agents_coord[worker]
                coord = (workers[worker][0],workers[worker][1])
                trajectset[worker].add(coord)
                wk_total_rwd[worker] += rwd[worker]
                epi_total_rwd += rwd[worker]
        print(epi_total_rwd)
        #updatemap
        infomap = updatemap(infomap,trajectset,env.SIZE,wk_total_rwd)
        datalist.append({'episode':i,'total_reward':epi_total_rwd})
    # print(datalist[999])
    # with open('ant.csv', 'w') as file:
    #     header = ['episode','total_reward']
    #     # Create a CSV dictionary writer and add the student header as field names
    #     writer = csv.DictWriter(file, fieldnames=header)
    #     # Use writerows() not writerow()
    #     writer.writeheader()
    #     writer.writerows(datalist)
    with open('anttrac.csv',"w") as file:
        header = ['time','x','y']
        writer = csv.DictWriter(file,fieldnames=header)
        writer.writeheader()
        writer.writerows(traclist)
    print(env.count)