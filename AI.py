import gym 
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete 
import numpy as np
import random
import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy
from datetime import datetime, timedelta
from components.SetTimer import GetTimer

class AI(Env):
    def __init__(self):
        # the shape of the data  being input
        self.shape = (208, 400)
        # Actions we can take, None, Trade, Buy/Sell, SL pips over 2 +/- .2
        self.action_space = MultiDiscrete([4, 100, 2, 300, 500])
        # allowed matrix of input data
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=self.shape, dtype=np.float32)
        # Set with the inital price data
        self.state = []

        # init variables
        self.nextCollectionTime = datetime.now()
        self.proccesable = False
        self.inTrade = False
        self.runningTicks = 0
        self.under1Min = False 
        self.reward = 0
    
    def SetNextCollectionTime(self, nextCollectionTime):
        self.nextCollectionTime = nextCollectionTime

    def setState(self, priceData):
        print('priceData ----------------------------')
        print(priceData)
        self.state = priceData
        self.proccesable = True
        
    def step(self, action):
        print(action)
        currentTime = datetime.now()
        while(not self.proccesable):
            GetTimer(currentTime, self.nextCollectionTime)
        self.proccesable = False
        
        # if not in trade reset datetime 
        self.tradeStartTime = currentTime.now()
        # --todo--
        # check if data is proccesable
        # if so then wait until next data has been put in
        # if not continue
        

        # Check if trade is done
        if self.state[0].open_trade_count == 0 or deltaTime >= 1800 : 
            done = True

        else:
            done = False


        # --todo--
        # Calculate reward
        reward = 0
        print('self.state[0] ----------------------------')
        print(self.state[0])
        reward += int((self.state[0].current_balance - self.state[1].current_balance) / self.state[1].current_balance ) # calcs based on percentage +/-
        deltaTime = abs((self.tradeStartTime - currentTime).total_seconds()) 
        if deltaTime >= 900: # calcs based on time over 15 mins
            reward += -.01 
        if deltaTime <= 60 and self.under1Min === False:
            reward += 1
            self.under1Min = True        


        # --todo-- 
        # if in trade do this
        # else do this
            


        
        # Set placeholder for info
        info = {}
        
        # Return step information
        return self.state, reward, done, info

    def render(self):
        # Implement viz
        pass
    
    def reset(self):
        self.runningTicks = 0 
        self.under1Min = False
        self.inTrade = False
        self.reward = 0
        return self.runningTicks
