import gym

from stable_baselines3 import PPO

from AI import AI

class AIModel():
    def __init__(self):
        self.env = AI()
        self.model = PPO("MlpPolicy", self.env, verbose=1)

    def Start(self, total_timesteps):
        print(f'total_timesteps: {total_timesteps}')
        self.model.learn(total_timesteps=total_timesteps)

    def GetEnv(self):
        return self.env