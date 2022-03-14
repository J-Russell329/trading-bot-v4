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
        self.shape = (400, 206)
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
        self.tradeStartTime = datetime.now()
        self.currentAccount = {
                'units':0,
                'max_potential_loss':0,
                'max_potential_loss_percentage': 0,
                'orders': 0,
                'positions': 0,
                'trades': 0,
                'position' : 0
                }
        # print(self)
    
    def SetNextCollectionTime(self, nextCollectionTime):
        self.nextCollectionTime = nextCollectionTime

    def setState(self, priceData, currentAccount):
        # print('priceData ----------------------------')
        # print(priceData)
        self.state = priceData
        self.currentAccount = currentAccount
        self.proccesable = True

    def setBot(self, bot):
        self.bot = bot

        
    def step(self, action):
        # print('steping in AI')
        currentTime = datetime.now()
        # print(f'currentTime: {currentTime}')
        # print(f'nextCollectionTime: {self.nextCollectionTime}')
        reward = 0
        done = False
        while(not self.proccesable):
            GetTimer(currentTime, self.nextCollectionTime)
        # print('out of wait loop in AI')
        self.proccesable = False

        # print(type(action)) # prints current action
        usableAction = action.tolist()
        tempNum = 0
        for action in usableAction: #changes usable action from string to int's
            if tempNum == 1:
                action += 1
            usableAction[tempNum] = int(action)

            tempNum += 1
        # print(usableAction) # prints current usableAction
        # print(type(usableAction)) # prints current usableAction

        # print('self state of 0  --------------------------------------')
        # print(self.state[0])
        
        if self.state[0][20] > 0:
            self.inTrade = True
        elif self.state[0][20] == 0:
            self.tradeStartTime = datetime.now()

        # --------------------in trade logic ------------------------
        if self.inTrade:
            deltaTime = abs((self.tradeStartTime - currentTime).total_seconds()) 

            # adds true if trade has ended
            if self.state[0][20] == 0 and self.state[1][20] > 0: 
                self.endTradeTick = True

            # adds true if trade has gone past 15 mins
            if deltaTime >= 1800 :
                self.past15Mins = True
            
            # the done statment 
            if self.endTradeTick:
                done = True

            # --------------------in trade reward logic ------------------------
            reward = int((self.state[0][16] - self.state[1][16]) / self.state[1][16] ) # calcs based on percentage +/-
            if deltaTime >= 900: # calcs based on time over 15 mins
                reward += -.01 
            if deltaTime <= 60 and self.under1Min == False:
                reward += 1
                self.under1Min = True
            if self.endTradeTick and deltaTime >= 900:
                reward += 1
            if usableAction[0] == 1 and self.currentAccount['max_potential_loss_percentage'] > 2.5:
                reward += -.05

            # force end trade after 30mins do not put in new action
            if deltaTime >= 3600:
                self.bot.CancelAllOrders()
                self.reset()

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
            
            if not done:
                print('--in trade--')
                # print(f"in trade: current max_potential_loss_percentage: {self.currentAccount['max_potential_loss_percentage']}")
                actionTradePosition = 'long' if usableAction[2] == 0 else 'short'
                # LoweringCurrentPosition is true if self.currentAccount['position'] != actionTradePosition
                LoweringCurrentPosition = False if self.currentAccount['position'] == actionTradePosition else True
                if usableAction[0] == 1:
                    if self.currentAccount['max_potential_loss_percentage'] < 2.5 or LoweringCurrentPosition:
                        print('should buy/sell positions')
                        self.bot.AddToOrder(
                            usableAction[1],
                            usableAction[2]
                        )
                elif usableAction[0] == 2:
                    print('should update orders to uniform sl and tp')
                    self.bot.UpdateOrder(
                        usableAction[3],
                        usableAction[4]
                    )
                elif usableAction[0] == 3 or self.past15Mins:
                    print('should be selling everything')
                    # self.bot.CancelAllOrders()
                    # self.reset()
                else:
                    print('no action taken')
                
            else:
                print('ai is done with this session')


            

        else:
            # Out of position [
            # int  (0,1, 2, 3 (wait or place order, Null , Null)),
            # Float (0-1 (% to trade)),
            # Int (0,1 (buy or sell)),
            # int (0-30 (number of SL pips over 2 ))
            # int (0-100 (number of take profit pips over 2 ))
            # ]
            print('--not in trade--')
            if usableAction[0]:
                self.bot.PlaceOrder(
                    usableAction[1],
                    usableAction[2],
                    usableAction[3],
                    usableAction[4]
                )

        print(usableAction) # prints current usableAction
        




        
        # Set placeholder for info
        info = {}
        
        # Return step information
        print(f"units: {self.currentAccount['units']}")
        print(f"max_potential_loss: {self.currentAccount['max_potential_loss']}")
        print(f"max_potential_loss_percentage: {self.currentAccount['max_potential_loss_percentage']}")
        return self.state, reward, done, info

    def render(self):
        # Implement viz
        pass
    
    def reset(self):
        print('reseting model')
        self.inTrade = False
        self.under1Min = False 
        self.endTradeTick = False
        self.past15Mins = False
        return self.state if self.state else 0
