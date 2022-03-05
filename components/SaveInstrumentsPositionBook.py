from models import Session, PositionBook
def SaveInstrumentsPositionBook(high, low, time, positionReport):
    high = high + .01
    low = low - .01
    newHighOrder = PositionBook()
    newHighOrder.timestamp = time
    newHighOrder.price = high
    newHighOrder.buy = 0
    newHighOrder.sell = 0
    newLowOrder = PositionBook()
    newLowOrder.timestamp = time
    newLowOrder.price = low
    newLowOrder.buy = 0
    newLowOrder.sell = 0

    dbInstrumentsPositionBook = Session()
    for order in positionReport['buckets']:
        if( float(order['price']) >= high):
            newHighOrder.buy += float(order['longCountPercent'])
            newHighOrder.sell += float(order['shortCountPercent'])
        elif (float(order['price']) <= low):
            newLowOrder.buy += float(order['longCountPercent'])
            newLowOrder.sell += float(order['shortCountPercent'])
        else:
            newOrder = PositionBook()
            newOrder.timestamp = time
            newOrder.price = order['price']
            newOrder.buy = order['longCountPercent']
            newOrder.sell = order['shortCountPercent']
            dbInstrumentsPositionBook.add(newOrder)
        
    dbInstrumentsPositionBook.add(newHighOrder)
    dbInstrumentsPositionBook.add(newLowOrder)
    dbInstrumentsPositionBook.commit()

