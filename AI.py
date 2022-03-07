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
        self.shape = (400, 205)
        # Actions we can take, None, Trade, Buy/Sell, SL pips over 2 +/- .2
        self.action_space = MultiDiscrete([4, 100, 2, 300, 500])
        # allowed matrix of input data
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=self.shape, dtype=np.float32)
        # Set with the inital price data
        self.state = []

        # init variables
        self.nextCollectionTime = datetime.now()
        self.api= None
        self.proccesable = False
        self.inTrade = False
        self.under1Min = False 
        self.endTradeTick = False
        self.past15Mins = False
        print(self)
    
    def SetNextCollectionTime(self, nextCollectionTime):
        self.nextCollectionTime = nextCollectionTime

    def setState(self, priceData):
        # print('priceData ----------------------------')
        # print(priceData)
        self.state = priceData
        self.proccesable = True

    def setBot(self, bot):
        self.bot = bot

        
    def step(self, action):
        reward = 0
        done = False
        currentTime = datetime.now()
        while(not self.proccesable):
            GetTimer(currentTime, self.nextCollectionTime)
        self.proccesable = False

        # print(action) # prints current action
        # print(type(action)) # prints current action
        # usableAction = action.tolist()
        print(usableAction) # prints current usableAction
        # print(type(usableAction)) # prints current usableAction

        if self.inTrade and self.state[1].open_trade_count > 0:
            self.tradeStartTime = currentTime.now()

        # --------------------in trade logic ------------------------
        if self.inTrade:
            deltaTime = abs((self.tradeStartTime - currentTime).total_seconds()) 

            # adds true if trade has ended
            if self.state[0].open_trade_count == 0 and self.state[1].open_trade_count > 0: 
                self.endTradeTick = True

            # adds true if trade has gone past 15 mins
            if deltaTime >= 1800 :
                self.past15Mins = True
            
            # the done statment 
            if endTradeTick:
                done = True

            # --------------------in trade reward logic ------------------------
            reward = int((self.state[0].current_balance - self.state[1].current_balance) / self.state[1].current_balance ) # calcs based on percentage +/-
            if deltaTime >= 900: # calcs based on time over 15 mins
                reward += -.01 
            if deltaTime <= 60 and self.under1Min == False:
                reward += 1
                self.under1Min = True
            if self.endTradeTick and deltaTime >= 900:
                reward += 1

            # force end trade after 30mins do not put in new action
            if deltaTime >= 3600:

                return self.state, reward, True, info

            # --todo-- 
            # if in trade do this
            # else do this
                
            
            # --------------------in trade action logic ------------------------
            # int  (0,1, 2, 3 (wait or place order, update SL and TP , drop position)),
            # int(0-100 (% to trade)),
            # Int (0,1 (buy or sell)),
            # int (0-30 (number of SL pips over 2 ))
            # int (0-100 (number of take profit pips over 2 ))
            # ]
            print('in trade')
            if usableAction[0] == 1:
                self.bot.PlaceOrder(
                    usableAction[1],
                    usableAction[2],
                    usableAction[3],
                    usableAction[4]
                )
            elif usableAction[0] == 2:
                self.bot.UpdateOrder(

                )
            elif usableAction[0] == 3:
                self.bot.CancelAllOrders()

            

        else:
            # Out of position [
            # int  (0,1, 2, 3 (wait or place order, Null , Null)),
            # Float (0-1 (% to trade)),
            # Int (0,1 (buy or sell)),
            # int (0-30 (number of SL pips over 2 ))
            # int (0-100 (number of take profit pips over 2 ))
            # ]
            print('not in trade')
            if usableAction[0]:
                self.bot.PlaceOrder(
                    float(usableAction[1]),
                    float(usableAction[2]),
                    float(usableAction[3]),
                    float(usableAction[4])
                )




        
        # Set placeholder for info
        info = {}
        
        # Return step information
        return self.state, reward, done, info

    def render(self):
        # Implement viz
        pass
    
    def reset(self):
        self.inTrade = False
        self.under1Min = False 
        self.endTradeTick = False
        self.past15Mins = False
        return self.state if self.state else 0
