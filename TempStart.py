from apscheduler.schedulers.blocking import BlockingScheduler
from TradingBot import *
import threading
import time

'''
creates instance of the trading bot and runs them 
'''
bot = TradingBot()
sched = BlockingScheduler()

@sched.scheduled_job('cron', hour='6', minute='0', timezone='America/Chicago')
def StartProcess():
    bot.running = True
    threading.Thread(target=bot.Start, args=(), group=None).start()

@sched.scheduled_job('cron', day_of_week='4', hour='14', minute='0', timezone='America/Chicago'')
def EndingProcess():
    threading.Thread(target=bot.EndingProcess, args=(), group=None).start()

sched.start()