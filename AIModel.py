import gym

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
import os
import boto3


from AI import AI

class AIModel():
    def __init__(self):
        self.env = AI()
        self.model = PPO("MlpPolicy", self.env, verbose=1)

    def Start(self, total_timesteps):
        # print(f'total_timesteps: {total_timesteps}')
        self.model.learn(total_timesteps=total_timesteps)

    def GetEnv(self):
        return self.env
    
    def Save(self):
        # print('saving model --------------------------------------------------------------------------------------')
        # print('saving model --------------------------------------------------------------------------------------')
        ppo_path = os.path.join('Training', 'Saved Models', 'PPO_Trade_AI')
        self.model.save(ppo_path)
        # print('saved model --------------------------------------------------------------------------------------')

        # s3 = boto3.resource('s3')
        # BUCKET = "test"

        # s3.Bucket(BUCKET).upload_file("your/local/file", "dump/file")
