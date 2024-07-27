import os
import numpy as np

import gymnasium as gym

import random
import cv2
import PIL
from PIL import Image

from ray.rllib.env.multi_agent_env import MultiAgentEnv, make_multi_agent
import torch as nn
import ray
from ray import air, tune
from ray.rllib.algorithms.ppo import PPOConfig
import argparse
from ray.rllib.models import ModelCatalog
from ray.rllib.utils.typing import MultiEnvDict
from ray.tune.registry import register_env
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2

from ray.rllib.env.env_context import EnvContext
from ray.rllib.utils.framework import try_import_tf, try_import_torch
from ray.rllib.utils.test_utils import check_learning_achieved
from ray.tune.logger import pretty_print
from ray.tune.registry import get_trainable_cls
from ray.rllib.policy.policy import PolicySpec
from ray.train import Checkpoint
from ray.rllib.algorithms.algorithm import Algorithm
from ray.tune import ExperimentAnalysis
'''
action 0 = up
action 1 = down
action 2 = left
action 3 = right

'''
#opencv的通道为gbr
white = (255, 255, 255)
black = (0, 0, 0)
azure = (139,139,139)
Green = (0, 255, 0)
Red = (0, 0, 255)
blue = (255, 0, 0)

NUM_ITERS = 100  # 最大时间步。原为100
NUM_PERIOD = 5 #周期

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
POT_COO = {'points_0': [3, 1], 'points_1': [3, 2], 'points_2': [3, 3], 
           'points_3': [3, 4], 'points_4': [3, 5], 'points_5': [4, 6], 
           'points_6': [4, 5], 'points_7': [5, 5], 'points_8': [5, 6],
           'points_9': [6, 4], 'points_10': [6, 5], 'points_11': [0, 4], 
           'points_12': [7, 3], 'points_13': [2,6], 'points_14': [8,3]}
PLA_COO7 = {'player_0': [1, 4], 'player_1': [2, 3], 'player_2': [7, 3], 'player_3': [3, 4], 'player_4': [2, 5] ,'player_5':[9,5],'player_6': [7, 5]}
PLA_COO8 = {'player_0': [1, 4], 'player_1': [2, 3], 'player_2': [7, 3], 'player_3': [3, 4], 'player_4': [2, 5] ,'player_5':[9,5],'player_6': [7, 5],'player_7': [4, 4]}
PLA_COO9 = {'player_0': [1, 4], 'player_1': [2, 3], 'player_2': [7, 3], 'player_3': [3, 4], 'player_4': [2, 5] ,'player_5':[9,5],'player_6': [7, 5],'player_7': [4, 4],'player_8': [6, 3]}
PLA_COO10 = {'player_0': [1, 4], 'player_1': [2, 3], 'player_2': [7, 3], 'player_3': [3, 4], 'player_4': [2, 5] ,'player_5':[9,5],'player_6': [7, 5],'player_7': [4, 4],'player_8': [6, 3],'player_9': [2, 7],}
PLA_COO = PLA_COO9
class raw_env(MultiAgentEnv):
    metadata = {
        "name": "customenvironment",
    }

    def __init__(self, render_mode=None, punish = 0, ptreward = 50,  workers = {}):
        ''''''
        """
        The init method takes in environment arguments and should define the following attributes:
        - possible_agents
        - action_spaces
        - observation_spaces
        These attributes should not be changed after initialization.

        """
        super().__init__()
        
        self.terminateds = set()
        self.truncateds = set()
        self.last_obs = {}
        self.last_rew = {}
        self.last_terminated = {}
        self.last_truncated = {}
        self.last_info = {}
        
        self.d={
        0:black,#bgcolor,10
        1:white,#prob1,5
        2:azure,#prob2,7
        3:Green,#point
        4:Red,#worker
        5:blue,#self
        }
        self.N_CHANNELS = 3
        self.SIZE = 10
        self.punish = punish
        self.ptreward = ptreward
        self.area = np.zeros([self.SIZE, self.SIZE], dtype=np.uint8)
        self.agents_coord = {}
        self.points_coord = {}
        self.rewardmap = np.zeros([self.SIZE, self.SIZE], dtype=np.uint8)
        self.agents = []
        self.render_mode = render_mode
        if workers == {}:
            nums = len(PLA_COO)
            self.agents = ["player_" + str(r) for r in range(nums)]
        else:
            pass
        self.last_obs = {agent: None for agent in self.agents}
        self._agent_ids = set(self.agents)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.SIZE, self.SIZE,self.N_CHANNELS), dtype= np.uint8)
        self.action_space = gym.spaces.Discrete(4)
        #for agent in self.agents:
            #self.observation_spaces[agent]=None

    def render(self):
        ''''''
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        渲染环境。在人工模式下，它可以打印到终端，打开
        打开一个图形窗口，或者打开一些人类可以看到和理解的其他显示。
        """
        if self.render_mode is None:
            gym.logger.warn(
                "You are calling render method without specifying any render mode."
            )
            return
        elif self.render_mode == 'human':
            img = self.get_image()
            img = Image.fromarray(img, 'RGB')
            img = img.resize((800,800))
            cv2.imshow('env',np.array(img))
            cv2.waitKey(2000)


    def reset(self, seed=None, return_info=False, options=None, points = [], map = None, workers={}):
        ''''''
        """
        Reset needs to initialize the `agents` attribute and must set up the
        environment so that render(), and step() can be called without issues.
        Here it initializes the `num_moves` variable which counts the number of
        hands that are played.
        Returns the observations for each agent
        """
        self.count = np.zeros([self.SIZE, self.SIZE], dtype=np.uint)
        self.num_moves = 1
        self.terminateds = set()
        self.truncateds = set()
        self.last_obs = {}
        self.last_rew = {}
        self.last_terminated = {}
        self.last_truncated = {}
        self.last_info = {}
        
        
        if map == None:
            '''
            for i in range(self.SIZE):
                arr =  self.area[i,:]
                for j in range(self.SIZE):
                    prob = random.randint(0,9)
                    if prob == 1:
                        arr[j] = 5 #10%
                    elif prob == 2 or prob == 3 or prob == 4:#20%
                        arr[j] = 7
                    else:
                        arr[j] = 10
            '''
            self.area = AREA
            
        else:
            pass
        if workers == {}:
            for agent in self.agents:
                '''
                self.agents_coord[agent] = [random.randint(0,self.SIZE-1),random.randint(0,self.SIZE-1)]
                '''
                self.agents_coord[agent] = [0,0]
                self.agents_coord[agent][0] = PLA_COO[agent][0]
                self.agents_coord[agent][1] = PLA_COO[agent][1]
        else:
            pass
        if points == []:
            nums = 15
            ptlist =[]
            for i in range(nums):
                '''
                pt = [random.randint(0,self.SIZE-1),random.randint(0,self.SIZE-1)]
                while pt in ptlist:
                    pt = [random.randint(0,self.SIZE-1),random.randint(0,self.SIZE-1)]
                ptlist.append(pt)
                self.points_coord['points_'+str(i)] = pt
                '''
                self.points_coord['points_'+str(i)] = POT_COO['points_'+str(i)]
        else:
            nums = len(points)
            ptlist = []
            for i in range(nums):
                self.points_coord['points_'+str(i)] = points[i]
        for point in self.points_coord:
            self.rewardmap[self.points_coord[point][0]][self.points_coord[point][1]] = self.ptreward
        for agent in self.agents:
            self.last_obs[agent] = self.get_image(worker = agent)
            self.last_terminated[agent] = False
            self.last_truncated[agent] = False
        self.state = self.get_image()

        self.last_info = {agent: {} for agent in self.agents}
        return self.last_obs, self.last_info

    def step(self, actions):
    
        ''''''
        """
        step(action) takes in an action for each agent and should return the
        - observations
        - rewards
        - terminations
        - truncations
        - infos
        dicts where each dict looks like {agent_1: item_1, agent_2: item_2}
        """
        # If a user passes in actions with no agents, then just return empty observations, etc.
        # 如果用户在没有智能体的情况下传入操作，那么只返回空的观察结果，等等。
        if not actions:
            self.agents = []
            return {}, {}, {}, {}, {}
        observations = {}
        rewards = {}
        terminateds = {}
        truncateds = {}
        # 这篇代码漏了state，要加上：
        for agent in self.agents:
            act = actions[agent]
            if act == 0:#up
                if self.agents_coord[agent][1] == 0:
                    current_point_coord = (self.agents_coord[agent][0],self.agents_coord[agent][1])
                    rewards[agent] = self.rewardmap[current_point_coord[0]][current_point_coord[1]]-self.punish
                    self.rewardmap[current_point_coord[0]][current_point_coord[1]] = 0
                else:
                    current_point_coord = (self.agents_coord[agent][0],self.agents_coord[agent][1])
                    target_point_coord = (self.agents_coord[agent][0],self.agents_coord[agent][1]-1)
                    current_point_situation = self.area[current_point_coord[0]][current_point_coord[1]]
                    target_point_situation = self.area[target_point_coord[0]][target_point_coord[1]]
                    prob = current_point_situation*target_point_situation
                    radnum = random.randint(1,100)
                    if radnum > prob:
                        rewards[agent] = self.rewardmap[current_point_coord[0]][current_point_coord[1]]-self.punish
                        self.rewardmap[current_point_coord[0]][current_point_coord[1]] = 0
                    if radnum <= prob:
                        self.agents_coord[agent][0] = target_point_coord[0]
                        self.agents_coord[agent][1] = target_point_coord[1]
                        rewards[agent] = self.rewardmap[target_point_coord[0]][target_point_coord[1]]-self.punish
                        self.rewardmap[target_point_coord[0]][target_point_coord[1]] = 0
            elif act == 1:#down
                if self.agents_coord[agent][1] == self.SIZE-1:
                    current_point_coord = (self.agents_coord[agent][0],self.agents_coord[agent][1])
                    rewards[agent] = self.rewardmap[current_point_coord[0]][current_point_coord[1]]-self.punish
                    self.rewardmap[current_point_coord[0]][current_point_coord[1]] = 0
                else:
                    current_point_coord = (self.agents_coord[agent][0],self.agents_coord[agent][1])
                    target_point_coord = (self.agents_coord[agent][0],self.agents_coord[agent][1]+1)
                    current_point_situation = self.area[current_point_coord[0]][current_point_coord[1]]
                    target_point_situation = self.area[target_point_coord[0]][target_point_coord[1]]
                    prob = current_point_situation*target_point_situation
                    radnum = random.randint(1,100)
                    if radnum > prob:
                        rewards[agent] = self.rewardmap[current_point_coord[0]][current_point_coord[1]]-self.punish
                        self.rewardmap[current_point_coord[0]][current_point_coord[1]] = 0
                    if radnum <= prob:
                        self.agents_coord[agent][0] = target_point_coord[0]
                        self.agents_coord[agent][1] = target_point_coord[1]
                        rewards[agent] = self.rewardmap[target_point_coord[0]][target_point_coord[1]]-self.punish
                        self.rewardmap[target_point_coord[0]][target_point_coord[1]] = 0
            elif act == 2:#left
                if self.agents_coord[agent][0] == 0:
                    current_point_coord = (self.agents_coord[agent][0],self.agents_coord[agent][1])
                    rewards[agent] = self.rewardmap[current_point_coord[0]][current_point_coord[1]]-self.punish
                    self.rewardmap[current_point_coord[0]][current_point_coord[1]] = 0
                else:
                    current_point_coord = (self.agents_coord[agent][0],self.agents_coord[agent][1])
                    target_point_coord = (self.agents_coord[agent][0]-1,self.agents_coord[agent][1])
                    current_point_situation = self.area[current_point_coord[0]][current_point_coord[1]]
                    target_point_situation = self.area[target_point_coord[0]][target_point_coord[1]]
                    prob = current_point_situation*target_point_situation
                    radnum = random.randint(1,100)
                    if radnum > prob:
                        rewards[agent] = self.rewardmap[current_point_coord[0]][current_point_coord[1]]-self.punish
                        self.rewardmap[current_point_coord[0]][current_point_coord[1]] = 0
                    if radnum <= prob:
                        self.agents_coord[agent][0] = target_point_coord[0]
                        self.agents_coord[agent][1] = target_point_coord[1]
                        rewards[agent] = self.rewardmap[target_point_coord[0]][target_point_coord[1]]-self.punish
                        self.rewardmap[target_point_coord[0]][target_point_coord[1]] = 0
            elif act == 3:#right
                if self.agents_coord[agent][0] == self.SIZE-1:
                    current_point_coord = (self.agents_coord[agent][0],self.agents_coord[agent][1])
                    rewards[agent] = self.rewardmap[current_point_coord[0]][current_point_coord[1]]-self.punish
                    self.rewardmap[current_point_coord[0]][current_point_coord[1]] = 0
                else:
                    current_point_coord = (self.agents_coord[agent][0],self.agents_coord[agent][1])
                    target_point_coord = (self.agents_coord[agent][0]+1,self.agents_coord[agent][1])
                    current_point_situation = self.area[current_point_coord[0]][current_point_coord[1]]
                    target_point_situation = self.area[target_point_coord[0]][target_point_coord[1]]
                    prob = current_point_situation*target_point_situation
                    radnum = random.randint(1,100)
                    if radnum > prob:
                        rewards[agent] = self.rewardmap[current_point_coord[0]][current_point_coord[1]]-self.punish
                        self.rewardmap[current_point_coord[0]][current_point_coord[1]] = 0
                    if radnum <= prob:
                        self.agents_coord[agent][0] = target_point_coord[0]
                        self.agents_coord[agent][1] = target_point_coord[1]
                        rewards[agent] = self.rewardmap[target_point_coord[0]][target_point_coord[1]]-self.punish
                        self.rewardmap[target_point_coord[0]][target_point_coord[1]] = 0
        # rewards for all agents are placed in the rewards dictionary to be returned
        # 所有代理的奖励都会放在要返回的奖励字典中
        for agent in self.agents:
            observations[agent] = self.get_image(worker=agent)
        if self.num_moves%NUM_PERIOD == 0:
            for point in self.points_coord:
                self.rewardmap[self.points_coord[point][0]][self.points_coord[point][1]] = self.ptreward
        if self.num_moves < NUM_ITERS:
            for agent in self.agents:
                terminateds[agent] = False
            self.num_moves += 1
        else:
            for agent in self.agents:
                terminateds[agent] = True
         
        if self.num_moves >= NUM_ITERS:
            env_truncation = True
        else:
            env_truncation = False
        for agent in self.agents:
            truncateds[agent] = env_truncation

        for agent in self.agents:
            self.count[self.agents_coord[agent][0]][self.agents_coord[agent][1]] +=1
        # typically there won't be any information in the infos, but there must
        # still be an entry for each agent
        # 通常情况下，信息（infos）中不会有任何信息，但每个代理都必须有一个条目
        self.infos = {agent: {} for agent in self.agents}
        self.state=self.get_image()
        for agent in self.agents:
            self.last_obs[agent] = observations[agent]
            self.last_rew[agent] = rewards[agent]
            self.last_terminated[agent] = terminateds[agent]
            self.last_truncated[agent] = truncateds[agent]
            self.last_info[agent] = self.infos[agent]
            if terminateds[agent] == True:
                self.terminateds.add(agent)
            if truncateds[agent] == True:
                self.truncateds.add(agent)
        terminateds["__all__"] = len(self.terminateds) == len(self.agents)
        truncateds["__all__"] = len(self.truncateds) == len(self.agents)
        if self.render_mode == "human":
            self.render()

        return observations, rewards, terminateds, truncateds, self.infos
    
    def get_image(self, worker = None):
        field = np.zeros((self.SIZE,self.SIZE,3), dtype=np.uint8)
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.area[i][j] == 10:
                    field[i][j] = self.d[0]
                elif self.area[i][j] == 7:
                    field[i][j] = self.d[2]
                elif self.area[i][j] == 5:
                    field[i][j] = self.d[1]
        for pt in self.points_coord:
            field[self.points_coord[pt][0]][self.points_coord[pt][1]] = self.d[3]
        for agent in self.agents:
            field[self.agents_coord[agent][0]][self.agents_coord[agent][1]] = self.d[4]

        if worker != None:
            field[self.agents_coord[worker][0]][self.agents_coord[worker][1]] = self.d[5]
        return field

    def observation_space_sample(self, agent_ids: list = None):
        dict = {}
        agentsset = []
        if agent_ids == None:
            agentsset = self.agents
        else:
            agentsset = agent_ids
        for agents in agentsset:
            dict[agents] = gym.spaces.Box(low=0, high=255, shape=(self.SIZE, self.SIZE, self.N_CHANNELS), dtype= np.uint8).sample()
        return dict
    def action_space_sample(self, agent_ids: list = None):
        dict = {}
        agentsset = []
        if agent_ids == None:
            agentsset = self.agents
        else:
            agentsset = agent_ids
        for agents in agentsset:
            dict[agents] = gym.spaces.Discrete(4).sample()
        return dict
    def action_space_contains(self, x):
        for agent in self.agents:
            if agent in x:
                pass
            else:
                return False
        return True
    def observation_space_contains(self, x):
        for agent in self.agents:
            if agent in x:
                pass
            else:
                return False
        return True


    



tf1, tf, tfv = try_import_tf()
torch, nn = try_import_torch()

parser = argparse.ArgumentParser()
parser.add_argument(
    "--run", type=str, default="PPO", help="The RLlib-registered algorithm to use."
)
parser.add_argument(
    "--framework",
    choices=["tf", "tf2", "torch"],
    default="torch",
    help="The DL framework specifier.",
)
parser.add_argument(
    "--as-test",
    action="store_true",
    help="Whether this script should be run as a test: --stop-reward must "
    "be achieved within --stop-timesteps AND --stop-iters.",
)
parser.add_argument(
    "--no-tune",
    action="store_true",
    help="Run without Tune using a manual train loop instead. In this case,"
    "use PPO without grid search and no TensorBoard.",
)
parser.add_argument(
    "--local-mode",
    action="store_true",
    help="Init Ray in local mode for easier debugging.",
)
parser.add_argument(
    "--stop-iters", type=int, default=200, help="Number of iterations to train."
)
parser.add_argument(
    "--stop-timesteps", type=int, default=200000, help="Number of timesteps to train."
)
parser.add_argument(
    "--stop-reward", type=float, default=150.0, help="Reward at which we stop training."
)
parser.add_argument("--num-cpus", type=int, default=0)



def env_creator():
        return raw_env()  # return an env instance

if __name__ == "__main__":
    args = parser.parse_args()
    print(f"Running with following CLI options: {args}")
    ray.init(local_mode=args.local_mode)
    # Can also register the env creator function explicitly with:
    # register_env("corridor", lambda config: SimpleCorridor(config))
    config = (PPOConfig().environment(raw_env,disable_env_checking=True,env_config={}).rollouts(num_rollout_workers=1).training(
            train_batch_size=512,
            lr=1e-3,
            gamma=0.9,
            lambda_=0.9,
            use_gae=True,
            clip_param=0.4,
            grad_clip=True,
            grad_clip_by="global_norm",
            entropy_coeff=0.1,
            vf_loss_coeff=0.25,
            sgd_minibatch_size=64,
            num_sgd_iter=10,
        ).debugging(log_level="ERROR").framework(framework="torch").multi_agent().resources(num_gpus=int(os.environ.get("RLLIB_NUM_GPUS", "0"))))
    checkpt = Checkpoint.from_directory("C:/Users/1/Desktop/testenv/custom-environment/env/ray_results/envname")
        
        
    stop = {
        "timesteps_total": args.stop_timesteps,
        "training_iteration": args.stop_iters,
    }
    checkpoint_config={"checkpoint_frequency": 5000,
                       "checkpoint_at_end":True
                       }
    if checkpt.get_metadata() == {}:
        print("false====================================================")
        tune.run(
        "PPO",
        name="PPO7",
        stop=stop,
        storage_path="C:/Users/1/Desktop/testenv/custom-environment/env/ray_results/envname",
        checkpoint_config = checkpoint_config,
        config=config.to_dict(),)


        pass
    else:
        analy = ExperimentAnalysis("C:/Users/1/Desktop/testenv/custom-environment/env/ray_results/envname")
        last_checkpoint = analy.get_last_checkpoint()
        my_new_ppo = Algorithm.from_checkpoint(last_checkpoint)
        tune.run(
        my_new_ppo,
        name="PPO",
        stop=stop,
        storage_path="C:/Users/1/Desktop/testenv/custom-environment/env/ray_results/envname",
        checkpoint_config = checkpoint_config,
        config=config.to_dict(),
        )
        print("true=====================================================")
        pass


    
