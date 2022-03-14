from oandapyV20 import API
from oandapyV20.endpoints.accounts import AccountDetails
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20.endpoints.transactions import TransactionsStream
from oandapyV20.endpoints.orders import OrderCreate
from oandapyV20.endpoints.positions import PositionClose
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
        self.currentBalance = 0
        self.max_potential_loss = 0
        self.margin_available = 0
        self.position = None
        self.lastest_price = {
            'ask': 0,
            'bid': 0,
            'spread': 0,
            'mid': 0
        }
        # self.running_nums = {
        #     'day_p_and_l' : 0,
        #     'day_pips': 0,
        #     'unrealized_p_and_l': 0,
        #     'unrealized_pips': 0,
        #     'position': 0,
        #     'avg_entry_price': 0,
        #     'lots': 0,
        #     'max_potential_loss': 0,
        #     'avg_stop_loss': 0,
        #     'avg_loss_pips': 0,
        #     'avg_take_profit': 0,
        #     'take_profit_pips': 0
        # }
        self.orders= []
        self.positions = []
        self.trades = []
        self.starting_balance = None
        self.AI = AI
        self.DataCollectedCount = 0 # --test-- change to 0 when push to prod
        self.AI.setBot(self)
        self.units = 0

    def Start(self):
        '''
        used to run all four instances of data gatheres
        synchronsouly
        '''
        print('checking for any open trades')
        print(self.BeforeTradeTradeCanceler())
        print('may the trades be in our favor')
        self.nextTimeStamp = datetime.now()
        self.running = True
        dbMain.rollback()
        threading.Thread(target=self.PricingStream, args=(), group=None).start()
        self.DailyBalanceUpdate()
        self.GetCurrentPrice()
        self.Timer()
        

    def EndingProcess(self):
        '''
        everything that needs to happen before killing the script 
        like running the training scripts
        '''
        self.running = False
        # --todo-- should add in logic to do stuff over the weekend
        print('happy trading day!')
        return "good trading!"
    
    def RestartStream(self):
        time.sleep(1)
        threading.Thread(target=self.PricingStream, args=(), group=None).start()
    
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
        self.starting_balance = data['account']['balance']


    def GetData(self):
        self.DataCollectedCount += 1
        bookData = BookWraper(
            self.api, self.instrument, self.nextTimeStamp, self.granularity, self.lastest_price, self.accountID,self.sessionStart, self.starting_balance,
            self.AI, self.DataCollectedCount, self.UpdateBotAccount, self.UpdateSLTP
            ).getData()


    def BeforeTradeTradeCanceler(self):
        r = AccountDetails(accountID=self.accountID)
        self.api.request(r)
        data = r.response
        self.positions = data['account']['positions'][0]
        returnString = 'no orders to cancel'
        if(int(self.positions['long']['units']) != 0):
            self.position= 'long'
            returnString = 'canceling long orders'
        elif (int(self.positions['short']['units']) != 0):
            self.position= 'short'
            returnString = 'canceling short orders'
        self.CancelAllOrders()
        return returnString
        
    
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
            self.RestartStream()
            print("Error with stream. restarting now")

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

    def UpdateSLTP(self, SL, TP):
        self.currentSLPrice = SL
        self.currentTPPrice = TP


    def UpdateBotAccount(self, currentBalance, max_potential_loss, margin_available, position, orders, positions, trades, units):
        self.currentBalance = float(currentBalance)
        self.max_potential_loss = max_potential_loss,
        self.margin_available = margin_available,
        self.position = position
        self.orders = orders
        self.positions = positions
        self.trades = trades
        self.units = units
        print(f'current position: {self.position}')

    def PlaceOrder(self, tradePercent, tradeType, SL, TP):
        try:
            print('placing init order')
            if tradePercent <= 0.01:
                print(f'skiping trade ---- percent too low: trade Percent {tradePercent}')
                return
            tradeUnitMultiplier = 1 if tradeType == 0 else -1
            maxCurrentTradeDollarLoss = self.currentBalance * (tradePercent * 0.000001) 

            units = int((maxCurrentTradeDollarLoss / SL) * 10000)
            if tradeType == 0:
                SLPrice = str( round(self.lastest_price['ask'] - (SL * 0.000001) - .002,5) )
                TPPrice = str( round(self.lastest_price['bid'] + (TP * 0.000001) + .002,5) )
            else:
                TPPrice = str( round(self.lastest_price['ask'] - (TP * 0.000001) - .002,5) )
                SLPrice = str( round(self.lastest_price['bid'] + (SL * 0.000001) + .002,5) )

            self.currentSLPrice = SLPrice
            self.currentTPPrice = TPPrice
            data = {
                "order": {
                    "stopLossOnFill": {
                        "price": SLPrice
                    },
                    "takeProfitOnFill": {
                        "price": TPPrice
                    },
                    "timeInForce": "FOK",
                    "instrument": self.instrument,
                    "units": max(units,1) * tradeUnitMultiplier,
                    "type": 'MARKET',
                    "positionFill": "DEFAULT"
                }
            }
            if units == 0:
                print(f'skiping trade ---- units = {units}')
                return

            
            r = OrderCreate(self.accountID, data=data)
            self.api.request(r)
            # print(r.response)
            # print('order placed')
        except:
            print('and error occured in TradingBot.PlaceOrder')
            print(f'SLPrice: {SLPrice} : {type(SLPrice)}')
            print(f'self.currentSLPrice: {self.currentSLPrice} : {type(self.currentSLPrice)}')
            print(f'TPPrice: {TPPrice} : {type(TPPrice)}')
            print(f'self.currentTPPrice: {self.currentTPPrice} : {type(self.currentTPPrice)}')
            print(f'units: {units} : {type(units)}')
            print(f'maxDollarLossForCurrentBalance: {maxDollarLossForCurrentBalance}')
            print(f'maxCurrentTradeDollarLoss: {maxCurrentTradeDollarLoss}')
            pass

    def AddToOrder(self, tradePercent, tradeType):
        try:
            openTradeUnits = self.units
            # tradeUnitMultiplier = 1 if long -1 if short
            tradeUnitMultiplier = 1 if tradeType == 0 else -1
            # tradeUnitMultiplier = max loss if this trade goes south
            maxCurrentTradeDollarLoss = self.currentBalance * (tradePercent * 0.00001)
            # maxDollarLossForCurrentBalance = reminder between current max loss and open position max loss
            maxDollarLossForCurrentBalance = (self.currentBalance * 0.025)
            # (currentBalance * 2.5%) (currentPrice - SLPrice {pips to SL})
            unitsRemaining = ((maxDollarLossForCurrentBalance / float(self.currentSLPrice)) * 10000) - openTradeUnits
            unitsCurrentTrade = (maxCurrentTradeDollarLoss / float(self.currentSLPrice)) * 10000
            units = min(unitsRemaining, unitsCurrentTrade)
            if units <= 0:
                print('passing becuase units is less than 0')
                return

            print('-----------------Adding to order ---------------------')
            print(f'maxDollarLossForCurrentBalance: {maxDollarLossForCurrentBalance}')
            print(f'maxCurrentTradeDollarLoss: {maxCurrentTradeDollarLoss}')
            print(f'unitsRemaining: {unitsRemaining}')
            print(f'unitsCurrentTrade: {unitsCurrentTrade}')
            print(f'units: {units}')
            print(f'openTradeUnits: {openTradeUnits}')
            print('---------------Adding to order ---------------------')
            data = {
                "order": {
                    "stopLossOnFill": {
                        "price": self.currentSLPrice
                    },
                    "takeProfitOnFill": {
                        "price": self.currentTPPrice
                    },
                    "timeInForce": "FOK",
                    "instrument": self.instrument,
                    "units": int(units * tradeUnitMultiplier),
                    "type": 'MARKET',
                    "positionFill": "DEFAULT"
                }
            }
            print(data)
            r = OrderCreate(self.accountID, data=data)
            self.api.request(r)
            # print(r.response)
            # print('added to order')
        except:
            print('and error occured in TradingBot.AddToOrder')
            print(f'units: {units} : {type(units)}')
            print(f'maxDollarLossForCurrentBalance: {maxDollarLossForCurrentBalance} : {type(maxDollarLossForCurrentBalance)}')
            print(f'maxCurrentTradeDollarLoss: {maxCurrentTradeDollarLoss} : {type(maxCurrentTradeDollarLoss)}')
            print(r.response)
            return

    def UpdateOrder(self, SL, TP):
        # pass
        print('this will update order')
        # print(f'SL: {SL}')
        # print(f'TP: {TP}')
        # print(self.trades)

    def CancelAllOrders(self):
        print('Canceling all orders')
        try:
            # print(f'position: {position}')
            if self.position == 'long':
                data = {"longUnits": "ALL"}
            elif self.position == 'short':
                data = {"shortUnits": "ALL"}
            else:
                return
            r = PositionClose(self.accountID,
                self.instrument,
                data = data
            )
            self.api.request(r)
            # print('-------------------close position-------------------')
            # print(f'data: {data}')
            # print(r.response)
        except:
            print('and error occured in TradingBot.CancelAllOrders')
            pass
        # print('trades have been canceled')
        # print('this is where trades are supposed to be canceled')
        # except:
            # print(f"trade with order id: {trade['id']} doesnt exist")



