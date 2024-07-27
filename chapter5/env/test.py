from mcsrlenv import raw_env 
from ray.rllib.models import ModelCatalog
import numpy as np
import torch as nn
import gymnasium as gym
from gymnasium.spaces import Discrete, Box
import random
import cv2
import PIL
import time
from PIL import Image
from ray.rllib.utils import check_env
from ray.train import Checkpoint
from ray.rllib.algorithms.algorithm import Algorithm
from ray.tune import ExperimentAnalysis
import netron
import csv
import os
def cal(num):
    total = 0
    count = 0
    ptlist = []
    for i in range(num):
        ptlist.append((random.randint(0,9),random.randint(0,9)))
    for i in range(num-1):
        for j in range(i+1,num):
            count += 1
            total += abs(ptlist[i][0]-ptlist[j][0])+abs(ptlist[i][1]-ptlist[j][1])
    return total/count
if __name__ == "__main__":
    env = raw_env()
    '''
    print(env.agents_coord)
    actions = {}
    print(env.agents)
    for agent in env.agents:
        actions[agent] = 3
        print(env.agents_coord[agent][1])
    env.step(actions)
    print(env.agents_coord)
    print(env.agents)
    #print(obs)
    print(obs[env.agents[0]].shape)
    print(Box(low=0, high=255, shape=(30, 30, 3), dtype= np.uint8).shape)
    for agent in env.agents:
        if obs[agent].shape == Box(low=0, high=255, shape=(30, 30, 3), dtype= np.uint8).shape:
            print("pass")
        else:
            print("not pass")
    print(env.observation_space_contains(obs))
    obs,infos = env.reset()
    print(env._agent_ids)
    '''
    #check_env(env)
    path = "C:/Users/1/Desktop/testenv/custom-environment/env/ray_results/envname/PPO9/PPO_raw_env_9ad74_00000_0_2024-06-01_18-56-31/checkpoint_000000"
    mypolicy = Algorithm.from_checkpoint(path)
    obs, info =env.reset()
    traclist = []
    totalrwd = 0
    for j in range(0,100):
        time = j
        cx = env.agents_coord[env.agents[0]][0]
        cy = env.agents_coord[env.agents[0]][1]
        traclist.append({'time':time,'x':cx,'y':cy})
        action ={}
        for agent in env.agents:
            action[agent]=mypolicy.compute_single_action(obs[agent])
        obs, rwd, ter, tru, info = env.step(action)
        for agent in env.agents:
            totalrwd += rwd[agent]
    with open('marltrac.csv',"w") as file:
        header = ['time','x','y']
        writer = csv.DictWriter(file,fieldnames=header)
        writer.writeheader()
        writer.writerows(traclist)
    print(env.count)
    print(totalrwd)



    
  



    



