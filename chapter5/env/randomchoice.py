import numpy as np
from mcsrlenv import raw_env
import os
import random
import csv

if __name__ == '__main__':
    env = raw_env()
    episodelimit = 1000
    datalist = []
    env.reset()
    for i in range(episodelimit):
        print("=========episode"+str(i))
        env.reset()
        workers = env.agents_coord
        points = env.points_coord
        actions = {}
        epi_total_rwd = 0
        for j in range(100):
            for worker in workers:
                act = random.randint(0,3)
                actions[worker] = act
            obs, rwd, ter, tru, inf = env.step(actions=actions)
            for worker in workers:
                workers[worker] = env.agents_coord[worker]
                epi_total_rwd += rwd[worker]
        #updatemap
        datalist.append({'episode':i,'total_reward':epi_total_rwd})
    
    with open('randomchoice.csv', 'w') as file:
        header = ['episode','total_reward']
        # Create a CSV dictionary writer and add the student header as field names
        writer = csv.DictWriter(file, fieldnames=header)
        # Use writerows() not writerow()
        writer.writeheader()
        writer.writerows(datalist)