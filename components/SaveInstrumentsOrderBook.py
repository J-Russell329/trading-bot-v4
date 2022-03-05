from models import Session, OrderBook

def SaveInstrumentsOrderBook(high, low, time, orderReport):
    high = high + .01
    low = low - .01
    newHighOrder = OrderBook()
    newHighOrder.timestamp = time
    newHighOrder.price = high
    newHighOrder.buy = 0
    newHighOrder.sell = 0
    newLowOrder = OrderBook()
    newLowOrder.timestamp = time
    newLowOrder.price = low
    newLowOrder.buy = 0
    newLowOrder.sell = 0
    dbInstrumentsOrderBook = Session()
    for order in orderReport['buckets']:
        if(float(order['price']) >= high):
            newHighOrder.buy += float(order['longCountPercent'])
            newHighOrder.sell += float(order['shortCountPercent'])
        elif (float(order['price']) <= low):
            newLowOrder.buy += float(order['longCountPercent'])
            newLowOrder.sell += float(order['shortCountPercent'])
        else:
            newOrder = OrderBook()
            newOrder.timestamp = time
            newOrder.price = order['price']
            newOrder.buy = order['longCountPercent']
            newOrder.sell = order['shortCountPercent']
            dbInstrumentsOrderBook.add(newOrder)
        
    dbInstrumentsOrderBook.add(newHighOrder)
    dbInstrumentsOrderBook.add(newLowOrder)
    dbInstrumentsOrderBook.commit()