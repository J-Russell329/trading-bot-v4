from oandapyV20.endpoints.instruments import InstrumentsCandles, InstrumentsOrderBook, InstrumentsPositionBook
from oandapyV20.endpoints.pricing import PricingInfo
from oandapyV20.endpoints.forexlabs import CommitmentsOfTraders, Spreads
from oandapyV20.endpoints.accounts import AccountInstruments, AccountDetails
from oandapyV20.exceptions import V20Error
from models import Book, Session
from datetime import datetime
from components.SaveBook import *
import threading

class BookWraper():
    def __init__(self, api, instrument, timestamp, granularity, lastest_price, accountID, sessionStart, startingBalance
    , AI, DataCollectedCount
    # , orders, positions, trades
    ):
        # --todo-- could proably shave off a few ms by puting data direclty into the model Book object
        self.AI = AI
        self.DataCollectedCount = DataCollectedCount
        self.allOrders= {}
        self.allTrades= {}
        self.units = 0
        self.startingBalance= startingBalance
        self.orders= []
        self.positions = []
        self.trades = []
        self.sessionStart = sessionStart.strftime("%Y/%m/%d %H:%M:%S")
        self.accountID = accountID
        self.api = api
        self.timestamp = timestamp
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.instrument = instrument
        self.granularity = granularity['string']
        self.granularity_seconds = granularity['seconds']
        self.ask = lastest_price['ask']
        self.bid = lastest_price['bid']
        self.spread = self.PriceToPips(lastest_price['spread'])
        self.mid = lastest_price['mid']
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.price_difference = None
        self.volatility = None
        self.volume = None
        self.current_balance = None
        self.marginable_funds = None
        self.margin_available = None
        self.open_trade_count = None
        self.open_position_count = None
        self.pending_order_count = None
        self.margin_rate = None
        self.day_p_and_l = 0
        self.day_pips = None
        self.unrealized_p_and_l = None
        self.unrealized_pips = None
        self.position = None
        self.avg_entry_price = None
        self.lots = None
        self.max_potential_loss = 0
        self.avg_stop_loss = 0
        self.avg_loss_pips = 0
        self.avg_take_profit = 0
        self.take_profit_pips = 0
        self.ma10 = None
        self.ma25 = None
        self.ma50 = None
        self.ma100 = None
        self.ma200 = None
        self.ma400 = None
        self.highest10 = None
        self.highest25 = None
        self.highest50 = None
        self.highest100 = None
        self.highest200 = None
        self.highest400 = None
        self.lowest10 = None
        self.lowest25 = None
        self.lowest50 = None
        self.lowest100 = None
        self.lowest200 = None
        self.lowest400 = None
        self.high_10_percent_10 = None
        self.high_10_percent_25 = None
        self.high_10_percent_50 = None
        self.high_10_percent_100 = None
        self.high_10_percent_200 = None
        self.high_10_percent_400 = None
        self.low_10_percent_10 = None
        self.low_10_percent_25 = None
        self.low_10_percent_50 = None
        self.low_10_percent_100 = None
        self.low_10_percent_200 = None
        self.low_10_percent_400 = None
        self.order_book_up_short_all = 0
        self.order_book_down_short_all = 0
        self.order_book_up_short_0 = 0
        self.order_book_down_short_0 = 0
        self.order_book_up_short_1 = 0
        self.order_book_down_short_1 = 0
        self.order_book_up_short_2 = 0
        self.order_book_down_short_2 = 0
        self.order_book_up_short_3 = 0
        self.order_book_down_short_3 = 0
        self.order_book_up_short_4 = 0
        self.order_book_down_short_4 = 0
        self.order_book_up_short_5 = 0
        self.order_book_down_short_5 = 0
        self.order_book_up_short_6 = 0
        self.order_book_down_short_6 = 0
        self.order_book_up_short_7 = 0
        self.order_book_down_short_7 = 0
        self.order_book_up_short_8 = 0
        self.order_book_down_short_8 = 0
        self.order_book_up_short_9 = 0
        self.order_book_down_short_9 = 0
        self.order_book_up_short_10 = 0
        self.order_book_down_short_10 = 0
        self.order_book_up_short_20 = 0
        self.order_book_down_short_20 = 0
        self.order_book_up_short_40 = 0
        self.order_book_down_short_40 = 0
        self.order_book_up_short_60 = 0
        self.order_book_down_short_60 = 0
        self.order_book_up_short_80 = 0
        self.order_book_down_short_80 = 0
        self.order_book_up_short_100 = 0
        self.order_book_down_short_100 = 0
        self.order_book_between_long = 0
        self.order_book_between_short = 0
        self.order_book_up_long_all = 0
        self.order_book_down_long_all = 0
        self.order_book_up_long_0 = 0
        self.order_book_down_long_0 = 0
        self.order_book_up_long_1 = 0
        self.order_book_down_long_1 = 0
        self.order_book_up_long_2 = 0
        self.order_book_down_long_2 = 0
        self.order_book_up_long_3 = 0
        self.order_book_down_long_3 = 0
        self.order_book_up_long_4 = 0
        self.order_book_down_long_4 = 0
        self.order_book_up_long_5 = 0
        self.order_book_down_long_5 = 0
        self.order_book_up_long_6 = 0
        self.order_book_down_long_6 = 0
        self.order_book_up_long_7 = 0
        self.order_book_down_long_7 = 0
        self.order_book_up_long_8 = 0
        self.order_book_down_long_8 = 0
        self.order_book_up_long_9 = 0
        self.order_book_down_long_9 = 0
        self.order_book_up_long_10 = 0
        self.order_book_down_long_10 = 0
        self.order_book_up_long_20 = 0
        self.order_book_down_long_20 = 0
        self.order_book_up_long_40 = 0
        self.order_book_down_long_40 = 0
        self.order_book_up_long_60 = 0
        self.order_book_down_long_60 = 0
        self.order_book_up_long_80 = 0
        self.order_book_down_long_80 = 0
        self.order_book_up_long_100 = 0
        self.order_book_down_long_100 = 0
        self.position_book_between_long = 0
        self.position_book_between_short = 0
        self.position_book_up_short_all = 0
        self.position_book_down_short_all = 0
        self.position_book_up_short_0 = 0
        self.position_book_down_short_0 = 0
        self.position_book_up_short_1 = 0
        self.position_book_down_short_1 = 0
        self.position_book_up_short_2 = 0
        self.position_book_down_short_2 = 0
        self.position_book_up_short_3 = 0
        self.position_book_down_short_3 = 0
        self.position_book_up_short_4 = 0
        self.position_book_down_short_4 = 0
        self.position_book_up_short_5 = 0
        self.position_book_down_short_5 = 0
        self.position_book_up_short_6 = 0
        self.position_book_down_short_6 = 0
        self.position_book_up_short_7 = 0
        self.position_book_down_short_7 = 0
        self.position_book_up_short_8 = 0
        self.position_book_down_short_8 = 0
        self.position_book_up_short_9 = 0
        self.position_book_down_short_9 = 0
        self.position_book_up_short_10 = 0
        self.position_book_down_short_10 = 0
        self.position_book_up_short_20 = 0
        self.position_book_down_short_20 = 0
        self.position_book_up_short_40 = 0
        self.position_book_down_short_40 = 0
        self.position_book_up_short_60 = 0
        self.position_book_down_short_60 = 0
        self.position_book_up_short_80 = 0
        self.position_book_down_short_80 = 0
        self.position_book_up_short_100 = 0
        self.position_book_down_short_100 = 0
        self.position_book_up_long_all = 0
        self.position_book_down_long_all = 0
        self.position_book_up_long_0 = 0
        self.position_book_down_long_0 = 0
        self.position_book_up_long_1 = 0
        self.position_book_down_long_1 = 0
        self.position_book_up_long_2 = 0
        self.position_book_down_long_2 = 0
        self.position_book_up_long_3 = 0
        self.position_book_down_long_3 = 0
        self.position_book_up_long_4 = 0
        self.position_book_down_long_4 = 0
        self.position_book_up_long_5 = 0
        self.position_book_down_long_5 = 0
        self.position_book_up_long_6 = 0
        self.position_book_down_long_6 = 0
        self.position_book_up_long_7 = 0
        self.position_book_down_long_7 = 0
        self.position_book_up_long_8 = 0
        self.position_book_down_long_8 = 0
        self.position_book_up_long_9 = 0
        self.position_book_down_long_9 = 0
        self.position_book_up_long_10 = 0
        self.position_book_down_long_10 = 0
        self.position_book_up_long_20 = 0
        self.position_book_down_long_20 = 0
        self.position_book_up_long_40 = 0
        self.position_book_down_long_40 = 0
        self.position_book_up_long_60 = 0
        self.position_book_down_long_60 = 0
        self.position_book_up_long_80 = 0
        self.position_book_down_long_80 = 0
        self.position_book_up_long_100 = 0
        self.position_book_down_long_100 = 0
        print(f'inside of bookWraper')
        print(f'AI: {self.AI}')
        print(f'Data Collection Count of: {self.DataCollectedCount}')

    def getData(self):
        getHistory = threading.Thread(target=self.GetHistory, args=(), group=None)
        getInstrumentsOrderBook = threading.Thread(target=self.GetInstrumentsOrderBook, args=(), group=None)
        getInstrumentsPositionBook =threading.Thread(target=self.GetInstrumentsPositionBook, args=(), group=None)
        getAccountDetails =threading.Thread(target=self.GetAccountDetails, args=(), group=None)

        getHistory.start()
        getInstrumentsOrderBook.start()
        getInstrumentsPositionBook.start()
        getAccountDetails.start()

        getHistory.join()
        getInstrumentsOrderBook.join()
        getInstrumentsPositionBook.join()
        getAccountDetails.join()
        
        return self.checkCompletion()

    def checkCompletion(self):
        # print(f'orders: {self.orders}')
        # print(f'positions: {self.positions}')
        # print(f'trades: {self.trades}')
        # run calc after all info is there
        # --todo-- push for ai to make choice
        calcHighLowAvg = threading.Thread(target=self.calcHighLowAvg, args=(), group=None)
        calcPAndL = threading.Thread(target=self.calcPAndL, args=(), group=None)

        calcHighLowAvg.start()
        calcPAndL.start()

        calcHighLowAvg.join()
        calcPAndL.join()

        SaveBook(self)
        print('book saved')
        if (self.DataCollectedCount > 0): #--test-- will change  0 to 400 when done
            self.AI.setState(self.GetLast400())
            print('ai instance ran')
        return self

    def GetLast400(self):
        modelsSession = Session()
        try:
            priceData = modelsSession.execute(
                    f"""
                    select * from books
                    order by created_at desc
                    limit 400
                    """
                    )
            return priceData.all()
        finally:
            modelsSession.close()
            
    def GetAccountDetails(self):
        r = AccountDetails(accountID=self.accountID)
        self.api.request(r)
        data = r.response
        self.current_balance = data['account']['balance']
        self.margin_rate = float(data['account']['marginRate'])*1000
        self.marginable_funds = data['account']['marginAvailable']
        self.margin_available = round(self.margin_rate * float(self.marginable_funds),2)
        self.open_trade_count = data['account']['openTradeCount']
        self.open_position_count = data['account']['openPositionCount']
        self.pending_order_count = data['account']['pendingOrderCount']
        self.orders= data['account']['orders']
        self.positions = data['account']['positions'][0]
        self.trades = data['account']['trades']
        self.day_p_and_l = float(self.startingBalance) - float(self.current_balance)
        if(float(self.positions['long']['units']) > 0):
            self.unrealized_p_and_l = self.positions['long']['unrealizedPL']
            self.position = 'long'
            self.avg_entry_price = self.positions['long']['averagePrice']
            self.units = self.positions['long']['units']
        elif (float(self.positions['short']['units']) > 0):
            self.unrealized_p_and_l = self.positions['short']['unrealizedPL']
            self.position = 'short'
            self.avg_entry_price = self.positions['short']['averagePrice']
            self.units = self.positions['short']['units']
        self.lots = float(self.units) / 100000
        self.max_potential_loss

        # print (r.response) 
        

    def GetHistory(self):
        '''
        --------------------info--------------------
        gets the history of a instrument once every granularity then returns
        {
            open, close, high, low, spread, volume, volitlity
        }
        '''
        time = self.timestamp.strftime("%m/%d/%YT%H:%M:%S")
        params= {
            "to": time,
            "count":1,
            "granularity": self.granularity
            }
        res = InstrumentsCandles(
            instrument=self.instrument,
            params=params
            )
        self.api.request(res)
        bar = res.response["candles"][0]
        self.open = bar['mid']['o']
        self.close = bar['mid']['c']
        self.high = bar['mid']['h']
        self.low = bar['mid']['l']
        self.price_difference = self.PriceToPips(float(self.open) - float(self.close))
        self.volatility = self.PriceToPips(float(self.high) - float(self.low))
        self.volume = bar['volume']


    def PipsToPrice(self, pips):
        return pips *.001
         
    def PriceToPips(self, price):
        return round(price,5) * 10000

    def GetInstrumentsOrderBook(self):
        '''
        --------------------info--------------------
        gets the order book of a instrument and puts it into the class
        '''
        time = self.timestamp
        bid = float(self.bid)
        ask = float(self.ask)
        r = InstrumentsOrderBook(
            instrument=self.instrument,
            )
        self.api.request(r)
        orderReport = r.response['orderBook']['buckets']
        for order in orderReport:
            if(float(order['price']) > bid):
                self.order_book_up_long_all += float(order['longCountPercent'])
                self.order_book_up_short_all += float(order['shortCountPercent'])
            elif(float(order['price']) < ask):
                self.order_book_down_long_all += float(order['longCountPercent'])
                self.order_book_down_short_all += float(order['shortCountPercent'])
            else:
                self.order_book_between_long += float(order['longCountPercent'])
                self.order_book_between_short += float(order['shortCountPercent'])

            if(float(order['price']) > bid and float(order['price']) < (bid + self.PipsToPrice(1))):
                self.order_book_up_long_0 += float(order['longCountPercent'])
                self.order_book_up_short_0 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(1)) and float(order['price']) < (bid + self.PipsToPrice(2))):
                self.order_book_up_long_1 += float(order['longCountPercent'])
                self.order_book_up_short_1 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(2)) and float(order['price']) < (bid + self.PipsToPrice(3))):
                self.order_book_up_long_2 += float(order['longCountPercent'])
                self.order_book_up_short_2 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(3)) and float(order['price']) < (bid + self.PipsToPrice(4))):
                self.order_book_up_long_3 += float(order['longCountPercent'])
                self.order_book_up_short_3 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(4)) and float(order['price']) < (bid + self.PipsToPrice(5))):
                self.order_book_up_long_4 += float(order['longCountPercent'])
                self.order_book_up_short_4 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(5)) and float(order['price']) < (bid + self.PipsToPrice(6))):
                self.order_book_up_long_5 += float(order['longCountPercent'])
                self.order_book_up_short_5 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(6)) and float(order['price']) < (bid + self.PipsToPrice(7))):
                self.order_book_up_long_6 += float(order['longCountPercent'])
                self.order_book_up_short_6 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(7)) and float(order['price']) < (bid + self.PipsToPrice(8))):
                self.order_book_up_long_7 += float(order['longCountPercent'])
                self.order_book_up_short_7 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(8)) and float(order['price']) < (bid + self.PipsToPrice(9))):
                self.order_book_up_long_8 += float(order['longCountPercent'])
                self.order_book_up_short_8 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(9)) and float(order['price']) < (bid + self.PipsToPrice(10))):
                self.order_book_up_long_9 += float(order['longCountPercent'])
                self.order_book_up_short_9 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(10)) and float(order['price']) < (bid + self.PipsToPrice(20))):
                self.order_book_up_long_10 += float(order['longCountPercent'])
                self.order_book_up_short_10 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(20)) and float(order['price']) < (bid + self.PipsToPrice(40))):
                self.order_book_up_long_20 += float(order['longCountPercent'])
                self.order_book_up_short_20 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(40)) and float(order['price']) < (bid + self.PipsToPrice(60))):
                self.order_book_up_long_40 += float(order['longCountPercent'])
                self.order_book_up_short_40 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(60)) and float(order['price']) < (bid + self.PipsToPrice(80))):
                self.order_book_up_long_60 += float(order['longCountPercent'])
                self.order_book_up_short_60 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(80)) and float(order['price']) < (bid + self.PipsToPrice(100))):
                self.order_book_up_long_80 += float(order['longCountPercent'])
                self.order_book_up_short_80 += float(order['shortCountPercent'])
            elif(float(order['price']) >= (bid + self.PipsToPrice(100))):
                self.order_book_up_long_100 += float(order['longCountPercent'])
                self.order_book_up_short_100 += float(order['shortCountPercent'])
            elif(float(order['price']) < ask and float(order['price']) > (ask - self.PipsToPrice(1))):
                self.order_book_down_long_0 += float(order['longCountPercent'])
                self.order_book_down_short_0 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(1)) and float(order['price']) > (ask - self.PipsToPrice(2))):
                self.order_book_down_long_1 += float(order['longCountPercent'])
                self.order_book_down_short_1 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(2)) and float(order['price']) > (ask - self.PipsToPrice(3))):
                self.order_book_down_long_2 += float(order['longCountPercent'])
                self.order_book_down_short_2 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(3)) and float(order['price']) > (ask - self.PipsToPrice(4))):
                self.order_book_down_long_3 += float(order['longCountPercent'])
                self.order_book_down_short_3 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(4)) and float(order['price']) > (ask - self.PipsToPrice(5))):
                self.order_book_down_long_4 += float(order['longCountPercent'])
                self.order_book_down_short_4 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(5)) and float(order['price']) > (ask - self.PipsToPrice(6))):
                self.order_book_down_long_5 += float(order['longCountPercent'])
                self.order_book_down_short_5 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(6)) and float(order['price']) > (ask - self.PipsToPrice(7))):
                self.order_book_down_long_6 += float(order['longCountPercent'])
                self.order_book_down_short_6 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(7)) and float(order['price']) > (ask - self.PipsToPrice(8))):
                self.order_book_down_long_7 += float(order['longCountPercent'])
                self.order_book_down_short_7 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(8)) and float(order['price']) > (ask - self.PipsToPrice(9))):
                self.order_book_down_long_8 += float(order['longCountPercent'])
                self.order_book_down_short_8 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(9)) and float(order['price']) > (ask - self.PipsToPrice(10))):
                self.order_book_down_long_9 += float(order['longCountPercent'])
                self.order_book_down_short_9 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(10)) and float(order['price']) > (ask - self.PipsToPrice(20))):
                self.order_book_down_long_10 += float(order['longCountPercent'])
                self.order_book_down_short_10 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(20)) and float(order['price']) > (ask - self.PipsToPrice(40))):
                self.order_book_down_long_20 += float(order['longCountPercent'])
                self.order_book_down_short_20 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(40)) and float(order['price']) > (ask - self.PipsToPrice(60))):
                self.order_book_down_long_40 += float(order['longCountPercent'])
                self.order_book_down_short_40 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(60)) and float(order['price']) > (ask - self.PipsToPrice(80))):
                self.order_book_down_long_60 += float(order['longCountPercent'])
                self.order_book_down_short_60 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(80)) and float(order['price']) > (ask - self.PipsToPrice(100))):
                self.order_book_down_long_80 += float(order['longCountPercent'])
                self.order_book_down_short_80 += float(order['shortCountPercent'])
            elif(float(order['price']) <= (ask - self.PipsToPrice(100))):
                self.order_book_down_long_100 += float(order['longCountPercent'])
                self.order_book_down_short_100 += float(order['shortCountPercent'])

        
    
    
    def GetInstrumentsPositionBook(self):
        '''
        --------------------info--------------------
        gets the position book of a instrument and puts it into the class
        '''
        time = self.timestamp
        bid = float(self.bid)
        ask = float(self.ask)
        r = InstrumentsPositionBook(
            instrument=self.instrument,
            )
        self.api.request(r)
        positionReport = r.response['positionBook']['buckets']
        for position in positionReport:
            if(float(position['price']) >= bid):
                self.position_book_up_long_all += float(position['longCountPercent'])
                self.position_book_up_short_all += float(position['shortCountPercent'])
            elif(float(position['price']) <= ask):
                self.position_book_down_long_all += float(position['longCountPercent'])
                self.position_book_down_short_all += float(position['shortCountPercent'])
            else:
                self.position_book_between_long += float(position['longCountPercent'])
                self.position_book_between_short += float(position['shortCountPercent'])

            if(float(position['price']) >= bid and float(position['price']) < (bid + self.PipsToPrice(1))):
                self.position_book_up_long_0 += float(position['longCountPercent'])
                self.position_book_up_short_0 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(1)) and float(position['price']) < (bid + self.PipsToPrice(2))):
                self.position_book_up_long_1 += float(position['longCountPercent'])
                self.position_book_up_short_1 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(2)) and float(position['price']) < (bid + self.PipsToPrice(3))):
                self.position_book_up_long_2 += float(position['longCountPercent'])
                self.position_book_up_short_2 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(3)) and float(position['price']) < (bid + self.PipsToPrice(4))):
                self.position_book_up_long_3 += float(position['longCountPercent'])
                self.position_book_up_short_3 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(4)) and float(position['price']) < (bid + self.PipsToPrice(5))):
                self.position_book_up_long_4 += float(position['longCountPercent'])
                self.position_book_up_short_4 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(5)) and float(position['price']) < (bid + self.PipsToPrice(6))):
                self.position_book_up_long_5 += float(position['longCountPercent'])
                self.position_book_up_short_5 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(6)) and float(position['price']) < (bid + self.PipsToPrice(7))):
                self.position_book_up_long_6 += float(position['longCountPercent'])
                self.position_book_up_short_6 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(7)) and float(position['price']) < (bid + self.PipsToPrice(8))):
                self.position_book_up_long_7 += float(position['longCountPercent'])
                self.position_book_up_short_7 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(8)) and float(position['price']) < (bid + self.PipsToPrice(9))):
                self.position_book_up_long_8 += float(position['longCountPercent'])
                self.position_book_up_short_8 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(9)) and float(position['price']) < (bid + self.PipsToPrice(10))):
                self.position_book_up_long_9 += float(position['longCountPercent'])
                self.position_book_up_short_9 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(10)) and float(position['price']) < (bid + self.PipsToPrice(20))):
                self.position_book_up_long_10 += float(position['longCountPercent'])
                self.position_book_up_short_10 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(20)) and float(position['price']) < (bid + self.PipsToPrice(40))):
                self.position_book_up_long_20 += float(position['longCountPercent'])
                self.position_book_up_short_20 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(40)) and float(position['price']) < (bid + self.PipsToPrice(60))):
                self.position_book_up_long_40 += float(position['longCountPercent'])
                self.position_book_up_short_40 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(60)) and float(position['price']) < (bid + self.PipsToPrice(80))):
                self.position_book_up_long_60 += float(position['longCountPercent'])
                self.position_book_up_short_60 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(80)) and float(position['price']) < (bid + self.PipsToPrice(100))):
                self.position_book_up_long_80 += float(position['longCountPercent'])
                self.position_book_up_short_80 += float(position['shortCountPercent'])
            elif(float(position['price']) >= (bid + self.PipsToPrice(100))):
                self.position_book_up_long_100 += float(position['longCountPercent'])
                self.position_book_up_short_100 += float(position['shortCountPercent'])
            elif(float(position['price']) <= ask and float(position['price']) > (ask - self.PipsToPrice(1))):
                self.position_book_down_long_0 += float(position['longCountPercent'])
                self.position_book_down_short_0 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(1)) and float(position['price']) > (ask - self.PipsToPrice(2))):
                self.position_book_down_long_1 += float(position['longCountPercent'])
                self.position_book_down_short_1 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(2)) and float(position['price']) > (ask - self.PipsToPrice(3))):
                self.position_book_down_long_2 += float(position['longCountPercent'])
                self.position_book_down_short_2 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(3)) and float(position['price']) > (ask - self.PipsToPrice(4))):
                self.position_book_down_long_3 += float(position['longCountPercent'])
                self.position_book_down_short_3 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(4)) and float(position['price']) > (ask - self.PipsToPrice(5))):
                self.position_book_down_long_4 += float(position['longCountPercent'])
                self.position_book_down_short_4 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(5)) and float(position['price']) > (ask - self.PipsToPrice(6))):
                self.position_book_down_long_5 += float(position['longCountPercent'])
                self.position_book_down_short_5 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(6)) and float(position['price']) > (ask - self.PipsToPrice(7))):
                self.position_book_down_long_6 += float(position['longCountPercent'])
                self.position_book_down_short_6 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(7)) and float(position['price']) > (ask - self.PipsToPrice(8))):
                self.position_book_down_long_7 += float(position['longCountPercent'])
                self.position_book_down_short_7 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(8)) and float(position['price']) > (ask - self.PipsToPrice(9))):
                self.position_book_down_long_8 += float(position['longCountPercent'])
                self.position_book_down_short_8 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(9)) and float(position['price']) > (ask - self.PipsToPrice(10))):
                self.position_book_down_long_9 += float(position['longCountPercent'])
                self.position_book_down_short_9 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(10)) and float(position['price']) > (ask - self.PipsToPrice(20))):
                self.position_book_down_long_10 += float(position['longCountPercent'])
                self.position_book_down_short_10 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(20)) and float(position['price']) > (ask - self.PipsToPrice(40))):
                self.position_book_down_long_20 += float(position['longCountPercent'])
                self.position_book_down_short_20 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(40)) and float(position['price']) > (ask - self.PipsToPrice(60))):
                self.position_book_down_long_40 += float(position['longCountPercent'])
                self.position_book_down_short_40 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(60)) and float(position['price']) > (ask - self.PipsToPrice(80))):
                self.position_book_down_long_60 += float(position['longCountPercent'])
                self.position_book_down_short_60 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(80)) and float(position['price']) > (ask - self.PipsToPrice(100))):
                self.position_book_down_long_80 += float(position['longCountPercent'])
                self.position_book_down_short_80 += float(position['shortCountPercent'])
            elif(float(position['price']) <= (ask - self.PipsToPrice(100))):
                self.position_book_down_long_100 += float(position['longCountPercent'])
                self.position_book_down_short_100 += float(position['shortCountPercent'])

    
    def getHighLowAvg(self,ticks):
        modelsSession = Session()

        try:  
            highLowAvg = modelsSession.execute(
                f"""
                SELECT
                min(low) as lowest,
                max(high) as highest,
                count(low) as count,
                AVG(CASE WHEN high > (high-ten_percent) then high END) as "high_mean",
                AVG(CASE WHEN low < (low+ten_percent) then low  END) as "low_mean",
                avg(close)
                FROM (
                SELECT low, high, close, timestamp, (high-low)/10 as ten_percent
                FROM books
                WHERE timestamp > '{self.sessionStart}' ORDER BY timestamp DESC LIMIT {ticks}
                ) as t1
                """
                )
            (high, low, count, high_mean, low_mean,avg) = highLowAvg.one()
            if (count == 10):
                self.highest10 = high
                self.lowest10 = low
                self.high_10_percent_10 = high_mean
                self.low_10_percent_10 = low_mean
                self.ma10 = avg
            elif (count == 25):
                self.highest25 = high
                self.lowest25 = low
                self.high_10_percent_25 = high_mean
                self.low_10_percent_25 = low_mean
                self.ma25 = avg
            elif (count == 50):
                self.highest50 = high
                self.lowest50 = low
                self.high_10_percent_50 = high_mean
                self.low_10_percent_50 = low_mean
                self.ma50 = avg
            elif (count == 100):
                self.highest100 = high
                self.lowest100 = low
                self.high_10_percent_100 = high_mean
                self.low_10_percent_100 = low_mean
                self.ma100 = avg
            elif (count == 200):
                self.highest200 = high
                self.lowest200 = low
                self.high_10_percent_200 = high_mean
                self.low_10_percent_200 = low_mean
                self.ma200 = avg
            elif (count == 400):
                self.highest400 = high
                self.lowest400 = low
                self.high_10_percent_400 = high_mean
                self.low_10_percent_400 = low_mean
                self.ma400 = avg
        finally:
            modelsSession.close()

        

    def calcHighLowAvg(self):
        print('starting calcMovAvgs')
        highLowAvg10 = threading.Thread(target=self.getHighLowAvg, kwargs= {'ticks':10}, group=None)
        highLowAvg25 = threading.Thread(target=self.getHighLowAvg, kwargs= {'ticks':25}, group=None)
        highLowAvg50 = threading.Thread(target=self.getHighLowAvg, kwargs= {'ticks':50}, group=None)
        highLowAvg100 = threading.Thread(target=self.getHighLowAvg, kwargs= {'ticks':100}, group=None)
        highLowAvg200 = threading.Thread(target=self.getHighLowAvg, kwargs= {'ticks':200}, group=None)
        highLowAvg400 = threading.Thread(target=self.getHighLowAvg, kwargs= {'ticks':400}, group=None)

        highLowAvg10.start()
        highLowAvg25.start()
        highLowAvg50.start()
        highLowAvg100.start()
        highLowAvg200.start()
        highLowAvg400.start()

        highLowAvg10.join()
        highLowAvg25.join()
        highLowAvg50.join()
        highLowAvg100.join()
        highLowAvg200.join()
        highLowAvg400.join()
        return


    def calcPAndL(self):
        dollarPerUnit = 10 / 100000
        allUnits = 0 
        avg_take_profit_amount = 0
        avg_loss_pips = 0
        # estSpreadCost = ((float(self.spread) / 2) * units) * dollarPerUnit

        for trade in self.trades:
            tradeID = str(trade['id'])
            self.allTrades[tradeID] = {
                'price': float(trade['price']),
                'currentUnits': int(trade['currentUnits']),
                'takeProfitOrderID': trade['takeProfitOrderID'] or None,
                'stopLossOrderID':trade['stopLossOrderID'] or None
            }
        
        for order in self.orders:
            orderID = str(order['id'])
            self.allOrders[orderID] = {
                'price': float(order['price']),
                'type':order['type'],
                'tradeID':order['tradeID']
            }

        for allTradeID in self.allTrades:
            print(allTradeID)
            allTrade= self.allTrades[allTradeID]
            stopLossPrice = self.allOrders[allTrade['stopLossOrderID']]['price']
            takeProfitPrice = self.allOrders[allTrade['takeProfitOrderID']]['price']
            estSpreadCost = ((float(self.spread) / 2) * allTrade['currentUnits']) * dollarPerUnit
            print(f"allTrade['price']: {allTrade['price']}")            
            print(f"stopLossPrice: {stopLossPrice}")            
            print(f"allTrade['currentUnits']: {allTrade['currentUnits']}")            
            print(f"dollarPerUnit: {dollarPerUnit}")            
            print(f"estSpreadCost: {estSpreadCost}")         
            avg_take_profit_amount += abs(allTrade['price']-takeProfitPrice)   
            avg_loss_pips += abs(allTrade['price']-stopLossPrice) 
            self.max_potential_loss += (abs(allTrade['price']-stopLossPrice) * allTrade['currentUnits'])
            self.avg_take_profit += (abs(allTrade['price']-takeProfitPrice) * allTrade['currentUnits']) - estSpreadCost


        self.take_profit_pips =  self.PriceToPips(avg_take_profit_amount)
        self.avg_loss_pips = self.PriceToPips(avg_loss_pips)


        # for trade in self.trades:
            # allUnits += trade['currentUnits']
        #     stopPrice = float(trade['stopLossOnFill']['price'])
        #     profitPrice = float(trade['takeProfitOnFill']['price'])
        #     print(f'estSpreadCost: {estSpreadCost}')
        #     take_profit_pips += self.PriceToPips(abs(initPrice-profitPrice))
        #     avg_loss_pips += (abs(initPrice-stopPrice) * units)
        
        # for order in self.orders:

        # self.max_potential_loss += (abs(initPrice-stopPrice) * units) * dollarPerUnit
        # self.avg_take_profit += ((abs(initPrice-profitPrice) * units) * dollarPerUnit) - estSpreadCost
        # self.take_profit_pips =  self.PriceToPips(take_profit_pips / allUnits) if take_profit_pips > 0 else 0
        # self.avg_loss_pips = self.PriceToPips(avg_loss_pips / allUnits) if avg_loss_pips > 0 else 0


