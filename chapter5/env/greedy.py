import numpy as np
from mcsrlenv import raw_env
import os
import random
import csv
import math
AREA = np.array( [[7,10,7,5,10,10,10,10,10,10],
                  [10,7,7,5,7,10,10,5,7,10],
                  [7,7,10,10,10,10,10,7,10,7],
                  [7,10,10,10,10,10,7,10,10,10],
                  [10,5,7,10,10,10,10,7,10,10],
                  [10,10,10,10,10,10,10,10,10,5],
                  [7,10,10,10,7,5,7,10,7,10],
                  [10,10,10,10,10,10,10,10,10,10],
                  [10,7,10,10,10,5,10,10,10,10],
                  [10,10,7,10,7,5,10,7,7,5]])
def getpoint(wkco,points,despt):
    mindis = 100000
    for pt in points:
        rand = random.random()
        if rand < 0.4:
            if pt in despt.values():
                continue
        dis = abs(points[pt][0]-wkco[0])+abs(points[pt][1]-wkco[1])
        if (dis < mindis) and (dis != 0):
            mindis = dis
            mindespt = pt
    return mindespt
def getaction(wkco,ptco):
    if (wkco[0] == ptco[0]) and (wkco[1]<ptco[1]):
        return 1
    elif (wkco[0] == ptco[0]) and (wkco[1]>ptco[1]):
        return 0
    elif (wkco[0] < ptco[0]) and (wkco[1]==ptco[1]):
        return 3
    elif (wkco[0] > ptco[0]) and (wkco[1]==ptco[1]):
        return 2
    elif (wkco[0] < ptco[0]) and (wkco[1]<ptco[1]):
        # down = AREA[wkco[0]][wkco[1]-1]
        # right = AREA[wkco[0]+1][wkco[1]]
        # if down >= right:
        rand = random.random()
        if rand < 0.5:
            return 1
        else:
            return 3
    elif (wkco[0] > ptco[0]) and (wkco[1] < ptco[1]):   
        # down = AREA[wkco[0]][wkco[1]-1]
        # left = AREA[wkco[0]-1][wkco[1]]
        # if down >= left:
        rand = random.random()
        if rand < 0.5:
            return 1
        else:
            return 2
    elif (wkco[0] > ptco[0]) and (wkco[1] > ptco[1]):   
        # up = AREA[wkco[0]][wkco[1]+1]
        # left = AREA[wkco[0]-1][wkco[1]]
        # if up >= left:
        rand = random.random()
        if rand < 0.5:
            return 0
        else:
            return 2
    elif (wkco[0] < ptco[0]) and (wkco[1] > ptco[1]):   
        # up = AREA[wkco[0]][wkco[1]+1]
        # right = AREA[wkco[0]+1][wkco[1]]
        # if up >= right:
        rand = random.random()
        if rand < 0.5:
            return 0
        else:
            return 3
if __name__ == '__main__':
    env = raw_env()
    episodelimit = 1000
    datalist = []
    traclist = []
    for i in range(episodelimit):
        print("=========episode"+str(i))
        traclist = []
        env.reset()
        workers = env.agents_coord
        points = env.points_coord
        despt = {}
        actdict = {}
        epi_total_rwd = 0
        for worker in workers:
            targetpt = getpoint(env.agents_coord[worker],points,despt)
            despt[worker] = targetpt
        for j in range(100):
            time = j
            cx = env.agents_coord[env.agents[0]][0]
            cy = env.agents_coord[env.agents[0]][1]
            traclist.append({'time':time,'x':cx,'y':cy})
            for worker in workers:
                if env.agents_coord[worker] == points[despt[worker]]:
                    newtargetpt = getpoint(env.agents_coord[worker],points,despt)
                    despt[worker] = newtargetpt
                act = getaction(env.agents_coord[worker],points[despt[worker]])
                actdict[worker] = act
            obs, rwd, ter, tru, inf = env.step(actions=actdict)
            for worker in workers:
                workers[worker] = env.agents_coord[worker]
            for worker in rwd:
                epi_total_rwd += rwd[worker]
        datalist.append({'episode':i,'total_reward':epi_total_rwd})
        print(epi_total_rwd)
    # print(datalist[999])
    # with open('greedy.csv', 'w') as file:
    #     header = ['episode','total_reward']
    #     # Create a CSV dictionary writer and add the student header as field names
    #     writer = csv.DictWriter(file, fieldnames=header)
    #     # Use writerows() not writerow()
    #     writer.writeheader()
    #     writer.writerows(datalist)
    with open('greedytrac.csv',"w") as file:
        header = ['time','x','y']
        writer = csv.DictWriter(file,fieldnames=header)
        writer.writeheader()
        writer.writerows(traclist)
    print(env.count)
        

                

