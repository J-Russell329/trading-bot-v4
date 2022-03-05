from models import Session, PriceBar
def SaveHistory(bar, granularity):
    dbSaveHistory = Session()
    newBar = PriceBar()
    newBar.open_timestamp = bar['time']
    newBar.open_price = bar['mid']['o']
    newBar.close_price = bar['mid']['c']
    newBar.high_price = bar['mid']['h']
    newBar.low_price = bar['mid']['l']
    newBar.price_difference = round(float(newBar.open_price) - float(newBar.close_price),5) * 100000
    newBar.volatility = round(float(newBar.high_price) - float(newBar.low_price),5) * 100000
    newBar.volume = bar['volume']
    newBar.timeframe = granularity
    dbSaveHistory.add(newBar)
    dbSaveHistory.commit()