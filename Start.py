from apscheduler.schedulers.blocking import BlockingScheduler
from TradingBot import *
import threading
import time
import AI from AI

'''
creates instance of the trading bot and runs them 
'''
bot = TradingBot()
AI = AI()
sched = BlockingScheduler()



@sched.scheduled_job('cron', day_of_week='6', hour='16', minute='0', timezone='America/Chicago')
def StartProcess():
    bot.running = True
    bot.DataCollectedCount = 0
    threading.Thread(target=bot.Start, kwargs={'instrument':'EUR_USD', 'granularity','S5', 'AI':AI}, group=None).start()
    # threading.Thread(target=bot.Start, args=(), group=None).start() # --todo-- this is where I start the model trainer



@sched.scheduled_job('cron', day_of_week='4', hour='14', minute='0', timezone='America/Chicago'')
def EndingProcess():
    threading.Thread(target=bot.EndingProcess, args=(), group=None).start()

sched.start()