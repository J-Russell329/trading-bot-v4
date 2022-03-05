from apscheduler.schedulers.blocking import BlockingScheduler
from TradingBot import *
import threading
import time
from datetime import datetime
from AIModel import AIModel

'''
creates instance of the trading bot and runs them 
'''
sched = BlockingScheduler()
model = AIModel()
AI = model.GetEnv()
bot = TradingBot('EUR_USD', 'S5', AI)
threading.Thread(target=bot.Start, args=(), group=None).start()
threading.Thread(target=model.Start, kwargs={'total_timesteps':100}, group=None).start() # --todo-- this is where I start the model trainer
# bot.Start




# @sched.scheduled_job('cron', hour='22', minute='30', timezone='America/Chicago')
# def StartProcess():
#     threading.Thread(target=bot.Start, args=(), group=None).start()
#     time.sleep(7200)
#     bot.EndingProcess

# @sched.scheduled_job('cron', minute='24', timezone='America/Chicago')
# def EndingProcess():
#     threading.Thread(target=bot.EndingProcess, args=(), group=None).start()

# @sched.scheduled_job('cron', minute='*', second='2', timezone='America/Chicago')
# def Checker():
#     print({
#         "datetime": datetime.now(),
#         "bid":bot.bid,
#         "ask":bot.ask,
#         "next":bot.nextTimeStamp,
#         "running":bot.running,
#     })

# sched.start()

# @sched.scheduled_job('cron', minute='*', timezone='America/Chicago')
# def StartProcess():
#     print('start')
#     time.sleep(60)
#     print('end')

# @sched.scheduled_job('cron', minute='*', second='30', timezone='America/Chicago')
# def EndingProcess():
#     print('should run inbetween')

# sched.start()






# @sched.Start('cron', minute='*', timezone='America/Chicago')
# def EndingProcess():
#     threading.Thread(target=bot.EndingProcess, args=(), group=None).start()



# posibly add in a method to start the aws training method 
# sched.add_job(bot.EndingProcess, 'cron', minute='*', timezone='America/Chicago')
# bot.Start()
# sched.add_job(bot.Start, 'cron', day_of_week='6', hour='16', minute='0', timezone='America/Chicago')
# sched.add_job(bot.EndingProcess, 'cron', day_of_week='4', hour='14', minute='0', timezone='America/Chicago')
# sched.add_job(bot.EndingProcess, 'cron', minute='9,19,29,39,49,59', timezone='America/Chicago')
# sched.add_job(bot.Test, 'cron', second='0,30', timezone='America/Chicago')

# bot.Test()
