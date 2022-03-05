from oandapyV20 import API
from oandapyV20.endpoints.accounts import AccountDetails
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20.endpoints.transactions import TransactionsStream
from datetime import datetime, timedelta, date
from models import dbMain, Session
from components.SetTimer import SetTimer
from components.BookWraper import *
from config import config
import json
import os
import time
import threading

class TradingBot():
    def __init__(self, instrument, granularity, AI):
        self.accountID =  os.environ.get("AccountID","101-001-8814059-003")
        self.api = API(
            access_token= os.environ.get("Access_token", "03a02ccc4c6ddcded3f9f511fad253d0-280d18eb70276dd89aec026dc276e98e"),
            environment = os.environ.get("environment", "practice")
        )
        self.instrument=instrument
        self.sessionStart = datetime.today()
        self.running = True
        self.granularity = {
            'string' : granularity,
            'list': {
                'S':1,
                'M':60,
                'H':3600
                },
            'seconds': 0
        }
        self.granularity['seconds'] = self.granularity['list'][self.granularity['string'][0]] *  int(self.granularity['string'][1::])
        self.nextTimeStamp =datetime.now()
        self.prevTimeStamp = self.nextTimeStamp
        self.lastest_price = {
            'ask': 0,
            'bid': 0,
            'spread': 0,
            'mid': 0
        }
        self.running_nums = {
            'day_p_and_l' : 0,
            'day_pips': 0,
            'unrealized_p_and_l': 0,
            'unrealized_pips': 0,
            'position': 0,
            'avg_entry_price': 0,
            'lots': 0,
            'max_potential_loss': 0,
            'avg_stop_loss': 0,
            'avg_loss_pips': 0,
            'avg_take_profit': 0,
            'take_profit_pips': 0
        }
        self.orders= []
        self.positions = []
        self.trades = []
        self.startingBalance = None
        self.AI = AI
        self.DataCollectedCount = 0
        # print(self.AI)

    def Start(self):
        '''
        used to run all four instances of data gatheres
        synchronsouly
        '''
        print('may the trades be in our favor')
        self.nextTimeStamp = datetime.now()
        self.running = True
        dbMain.rollback()
        threading.Thread(target=self.PricingStream, args=(), group=None).start()
        # threading.Thread(target=self.TransactionStream, args=(), group=None).start()
        self.DailyBalanceUpdate()
        self.GetCurrentPrice()

        # init the AI model
        # log_path = os.path.join('Training', 'Logs')
        # model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log=log_path)
        # model.learn(total_timesteps=86400)
        
        self.Timer()
        

    def EndingProcess(self):
        '''
        everything that needs to happen before killing the script 
        like running the training scripts
        '''
        self.running = False
        model.save('PPO')
        # --todo-- should add in logic to do stuff over the weekend
        print('happy trading day!')
        return "good trading!"
    
    def Timer(self):
        '''
        run once every granularity
        '''
        while(self.running):
            start = datetime.now()
            threading.Thread(target=self.GetData(), name='GetData', args=(), group=None).start()
            self.prevTimeStamp = self.nextTimeStamp
            collectionTimestamp = self.prevTimeStamp
            self.nextTimeStamp += timedelta(seconds=self.granularity['seconds'])
            self.AI.SetNextCollectionTime(self.nextTimeStamp)
            SetTimer(self.granularity['seconds'], start, collectionTimestamp)
        return
    
    def DailyBalanceUpdate(self):
        r = AccountDetails(accountID=self.accountID)
        self.api.request(r)
        data = r.response
        self.startingBalance = data['account']['balance']


    def GetData(self):
        self.DataCollectedCount += 1
        bookData = BookWraper(
            self.api, self.instrument, self.nextTimeStamp, self.granularity, self.lastest_price, self.accountID,self.sessionStart, self.startingBalance,
            self.AI, self.DataCollectedCount
            # self.orders, self.positions, self.trades
            ).getData()
        # --todo-- step the AI model

    
    def PricingStream(self):
        dbPrincingSteam = Session()
        res = PricingStream(accountID=self.accountID, params={"instruments":self.instrument})

        try:
            for R in self.api.request(res):
                # print(R)
                if (R['type'] == 'PRICE'):
                    self.lastest_price['bid'] = float(R['bids'][0]["price"])
                    self.lastest_price['ask'] = float(R['asks'][0]["price"])
                    self.lastest_price['spread'] = float(self.lastest_price['ask']) - float(self.lastest_price['bid'])
                    self.lastest_price['mid'] = (float(self.lastest_price['bid']) + float(self.lastest_price['ask'])) / 2
                if not self.running:
                    res.terminate("ending steam")

        except V20Error as e:
            print("Error: {}".format(e))


    # def TransactionStream(self):
    #     dbPrincingSteam = Session()
    #     res = TransactionsStream(accountID=self.accountID)

    #     try:
    #         for R in self.api.request(res):
    #             print(f'TransactionStream :{R}')
    #             if (R['type'] != 'HEARTBEAT'):
    #                 return
    #                 # --todo-- use this stream to update the transactions stream
    #                 # self.orders= R['account']['orders']
    #                 # self.positions = R['account']['positions']
    #                 # self.trades = R['account']['trades']
    #             if not self.running:
    #                 res.terminate("ending Transaction")

    #     except V20Error as e:
    #         print("Error: {}".format(e))


        # client = oandapyV20.API(access_token=...)
        # r = trans.TransactionsStream(accountID=...)
        # rv = client.request(r)
        # maxrecs = 5
        # try:
        #     for T in r.response:  # or rv ...
        #         print json.dumps(R, indent=4), ","
        #         maxrecs -= 1
        #         if maxrecs == 0:
        #             r.terminate("Got them all")
        # except StreamTerminated as e:
        #     print("Finished: {msg}".format(msg=e))

    
    def GetCurrentPrice(self):
        params = {
            "instruments": self.instrument
            }
        r = PricingInfo(accountID=self.accountID, params=params)
        rv = self.api.request(r)
        self.lastest_price['bid'] = float(r.response['prices'][0]['bids'][0]["price"])
        self.lastest_price['ask'] = float(r.response['prices'][0]['asks'][0]["price"])
        self.lastest_price['spread'] = float(self.lastest_price['ask']) - float(self.lastest_price['bid'])
        self.lastest_price['mid'] = (float(self.lastest_price['bid']) + float(self.lastest_price['ask'])) / 2

    # def GetInstrumentsOrderBook(self):
    #     '''
    #     --------------------info--------------------
    #     gets the history of a instrument once every 5 seconds then stores it in the db
    #     '''
    #     time = self.nextTimeStamp
    #     r = InstrumentsOrderBook(
    #         instrument=self.instrument,
    #         )
    #     self.api.request(r)
    #     threading.Thread(target=SaveInstrumentsOrderBook, args=(self.bid, self.ask, time, r.response['orderBook']), group=None).start()
        

    # def GetInstrumentsPositionBook(self):
    #     time = self.nextTimeStamp
    #     r = InstrumentsPositionBook(
    #         instrument=self.instrument,
    #         )
    #     self.api.request(r)
    #     threading.Thread(target=SaveInstrumentsPositionBook, args=(self.bid, self.ask, time, r.response['positionBook']), group=None).start()
    
    # def GetAccountInstruments(self):
    #     params = {
    #         "instruments": self.instrument
    #         }
    #     r = AccountInstruments(accountID=self.accountID, params=params)
    #     self.api.request(r)
    #     print (r.response) 

    

