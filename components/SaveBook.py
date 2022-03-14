from models import Session, Book
def SaveBook(data):
    dbSaveBook = Session()
    newBook = Book()
    newBook.starting_balance =        data.starting_balance
    newBook.timestamp =        data.timestamp
    newBook.created_at =        data.created_at 
    newBook.updated_at =        data.updated_at
    newBook.instrument =        data.instrument
    newBook.granularity =        data.granularity
    newBook.granularity_seconds =        data.granularity_seconds
    newBook.ask =        data.ask 
    newBook.bid =        data.bid 
    newBook.mid =        data.mid 
    newBook.spread =        data.spread
    newBook.open =        data.open
    newBook.close =        data.close
    newBook.high =        data.high
    newBook.low =        data.low
    newBook.price_difference =        data.price_difference
    newBook.volatility =        data.volatility
    newBook.volume =        data.volume
    newBook.current_balance =        data.current_balance
    newBook.margin_rate =        data.margin_rate
    newBook.margin_available = data.margin_available
    newBook.marginable_funds = data.marginable_funds
    newBook.open_trade_count =     data.open_trade_count
    newBook.open_position_count =     data.open_position_count
    newBook.pending_order_count =     data.pending_order_count
    newBook.day_p_and_l =        data.day_p_and_l
    newBook.day_pips =        data.day_pips
    newBook.unrealized_p_and_l =        data.unrealized_p_and_l
    newBook.unrealized_pips =        data.unrealized_pips
    newBook.position =        data.position
    newBook.avg_entry_price =        data.avg_entry_price
    newBook.lots =        data.lots
    newBook.units =        data.units
    newBook.max_potential_loss =        data.max_potential_loss
    newBook.avg_stop_loss =        data.avg_stop_loss
    newBook.avg_loss_pips =        data.avg_loss_pips
    newBook.avg_take_profit =        data.avg_take_profit
    newBook.take_profit_pips =        data.take_profit_pips
    newBook.ma10 =        data.ma10
    newBook.ma25 =        data.ma25
    newBook.ma50 =        data.ma50
    newBook.ma100 =        data.ma100
    newBook.ma200 =        data.ma200
    newBook.ma400 =        data.ma400
    newBook.highest10 =        data.highest10
    newBook.highest25 =        data.highest25
    newBook.highest50 =        data.highest50
    newBook.highest100 =        data.highest100
    newBook.highest200 =        data.highest200
    newBook.highest400 =        data.highest400
    newBook.lowest10 =        data.lowest10
    newBook.lowest25 =        data.lowest25
    newBook.lowest50 =        data.lowest50
    newBook.lowest100 =        data.lowest100
    newBook.lowest200 =        data.lowest200
    newBook.lowest400 =        data.lowest400
    newBook.high_10_percent_10 =        data.high_10_percent_10
    newBook.high_10_percent_25 =        data.high_10_percent_25
    newBook.high_10_percent_50 =        data.high_10_percent_50
    newBook.high_10_percent_100 =        data.high_10_percent_100
    newBook.high_10_percent_200 =        data.high_10_percent_200
    newBook.high_10_percent_400 =        data.high_10_percent_400
    newBook.low_10_percent_10 =        data.low_10_percent_10
    newBook.low_10_percent_25 =        data.low_10_percent_25
    newBook.low_10_percent_50 =        data.low_10_percent_50
    newBook.low_10_percent_100 =        data.low_10_percent_100
    newBook.low_10_percent_200 =        data.low_10_percent_200
    newBook.low_10_percent_400 =        data.low_10_percent_400
    newBook.order_book_up_short_all =        data.order_book_up_short_all
    newBook.order_book_down_short_all =        data.order_book_down_short_all
    newBook.order_book_up_short_0 =        data.order_book_up_short_0
    newBook.order_book_down_short_0 =        data.order_book_down_short_0
    newBook.order_book_up_short_1 =        data.order_book_up_short_1
    newBook.order_book_down_short_1 =        data.order_book_down_short_1
    newBook.order_book_up_short_2 =        data.order_book_up_short_2
    newBook.order_book_down_short_2 =        data.order_book_down_short_2
    newBook.order_book_up_short_3 =        data.order_book_up_short_3
    newBook.order_book_down_short_3 =        data.order_book_down_short_3
    newBook.order_book_up_short_4 =        data.order_book_up_short_4
    newBook.order_book_down_short_4 =        data.order_book_down_short_4
    newBook.order_book_up_short_5 =        data.order_book_up_short_5
    newBook.order_book_down_short_5 =        data.order_book_down_short_5
    newBook.order_book_up_short_6 =        data.order_book_up_short_6
    newBook.order_book_down_short_6 =        data.order_book_down_short_6
    newBook.order_book_up_short_7 =        data.order_book_up_short_7
    newBook.order_book_down_short_7 =        data.order_book_down_short_7
    newBook.order_book_up_short_8 =        data.order_book_up_short_8
    newBook.order_book_down_short_8 =        data.order_book_down_short_8
    newBook.order_book_up_short_9 =        data.order_book_up_short_9
    newBook.order_book_down_short_9 =        data.order_book_down_short_9
    newBook.order_book_up_short_10 =        data.order_book_up_short_10
    newBook.order_book_down_short_10 =        data.order_book_down_short_10
    newBook.order_book_up_short_20 =        data.order_book_up_short_20
    newBook.order_book_down_short_20 =        data.order_book_down_short_20
    newBook.order_book_up_short_40 =        data.order_book_up_short_40
    newBook.order_book_down_short_40 =        data.order_book_down_short_40
    newBook.order_book_up_short_60 =        data.order_book_up_short_60
    newBook.order_book_down_short_60 =        data.order_book_down_short_60
    newBook.order_book_up_short_80 =        data.order_book_up_short_80
    newBook.order_book_down_short_80 =        data.order_book_down_short_80
    newBook.order_book_up_short_100 =        data.order_book_up_short_100
    newBook.order_book_down_short_100 =        data.order_book_down_short_100
    newBook.order_book_between_long =        data.order_book_between_long
    newBook.order_book_between_short =        data.order_book_between_short
    newBook.order_book_up_long_all =        data.order_book_up_long_all
    newBook.order_book_down_long_all =        data.order_book_down_long_all
    newBook.order_book_up_long_0 =        data.order_book_up_long_0
    newBook.order_book_down_long_0 =        data.order_book_down_long_0
    newBook.order_book_up_long_1 =        data.order_book_up_long_1
    newBook.order_book_down_long_1 =        data.order_book_down_long_1
    newBook.order_book_up_long_2 =        data.order_book_up_long_2
    newBook.order_book_down_long_2 =        data.order_book_down_long_2
    newBook.order_book_up_long_3 =        data.order_book_up_long_3
    newBook.order_book_down_long_3 =        data.order_book_down_long_3
    newBook.order_book_up_long_4 =        data.order_book_up_long_4
    newBook.order_book_down_long_4 =        data.order_book_down_long_4
    newBook.order_book_up_long_5 =        data.order_book_up_long_5
    newBook.order_book_down_long_5 =        data.order_book_down_long_5
    newBook.order_book_up_long_6 =        data.order_book_up_long_6
    newBook.order_book_down_long_6 =        data.order_book_down_long_6
    newBook.order_book_up_long_7 =        data.order_book_up_long_7
    newBook.order_book_down_long_7 =        data.order_book_down_long_7
    newBook.order_book_up_long_8 =        data.order_book_up_long_8
    newBook.order_book_down_long_8 =        data.order_book_down_long_8
    newBook.order_book_up_long_9 =        data.order_book_up_long_9
    newBook.order_book_down_long_9 =        data.order_book_down_long_9
    newBook.order_book_up_long_10 =        data.order_book_up_long_10
    newBook.order_book_down_long_10 =        data.order_book_down_long_10
    newBook.order_book_up_long_20 =        data.order_book_up_long_20
    newBook.order_book_down_long_20 =        data.order_book_down_long_20
    newBook.order_book_up_long_40 =        data.order_book_up_long_40
    newBook.order_book_down_long_40 =        data.order_book_down_long_40
    newBook.order_book_up_long_60 =        data.order_book_up_long_60
    newBook.order_book_down_long_60 =        data.order_book_down_long_60
    newBook.order_book_up_long_80 =        data.order_book_up_long_80
    newBook.order_book_down_long_80 =        data.order_book_down_long_80
    newBook.order_book_up_long_100 =        data.order_book_up_long_100
    newBook.order_book_down_long_100 =        data.order_book_down_long_100
    newBook.position_book_between_long =        data.position_book_between_long
    newBook.position_book_between_short =        data.position_book_between_short
    newBook.position_book_up_short_all =        data.position_book_up_short_all
    newBook.position_book_down_short_all =        data.position_book_down_short_all
    newBook.position_book_up_short_0 =        data.position_book_up_short_0
    newBook.position_book_down_short_0 =        data.position_book_down_short_0
    newBook.position_book_up_short_1 =        data.position_book_up_short_1
    newBook.position_book_down_short_1 =        data.position_book_down_short_1
    newBook.position_book_up_short_2 =        data.position_book_up_short_2
    newBook.position_book_down_short_2 =        data.position_book_down_short_2
    newBook.position_book_up_short_3 =        data.position_book_up_short_3
    newBook.position_book_down_short_3 =        data.position_book_down_short_3
    newBook.position_book_up_short_4 =        data.position_book_up_short_4
    newBook.position_book_down_short_4 =        data.position_book_down_short_4
    newBook.position_book_up_short_5 =        data.position_book_up_short_5
    newBook.position_book_down_short_5 =        data.position_book_down_short_5
    newBook.position_book_up_short_6 =        data.position_book_up_short_6
    newBook.position_book_down_short_6 =        data.position_book_down_short_6
    newBook.position_book_up_short_7 =        data.position_book_up_short_7
    newBook.position_book_down_short_7 =        data.position_book_down_short_7
    newBook.position_book_up_short_8 =        data.position_book_up_short_8
    newBook.position_book_down_short_8 =        data.position_book_down_short_8
    newBook.position_book_up_short_9 =        data.position_book_up_short_9
    newBook.position_book_down_short_9 =        data.position_book_down_short_9
    newBook.position_book_up_short_10 =        data.position_book_up_short_10
    newBook.position_book_down_short_10 =        data.position_book_down_short_10
    newBook.position_book_up_short_20 =        data.position_book_up_short_20
    newBook.position_book_down_short_20 =        data.position_book_down_short_20
    newBook.position_book_up_short_40 =        data.position_book_up_short_40
    newBook.position_book_down_short_40 =        data.position_book_down_short_40
    newBook.position_book_up_short_60 =        data.position_book_up_short_60
    newBook.position_book_down_short_60 =        data.position_book_down_short_60
    newBook.position_book_up_short_80 =        data.position_book_up_short_80
    newBook.position_book_down_short_80 =        data.position_book_down_short_80
    newBook.position_book_up_short_100 =        data.position_book_up_short_100
    newBook.position_book_down_short_100 =        data.position_book_down_short_100
    newBook.position_book_up_long_all =        data.position_book_up_long_all
    newBook.position_book_down_long_all =        data.position_book_down_long_all
    newBook.position_book_up_long_0 =        data.position_book_up_long_0
    newBook.position_book_down_long_0 =        data.position_book_down_long_0
    newBook.position_book_up_long_1 =        data.position_book_up_long_1
    newBook.position_book_down_long_1 =        data.position_book_down_long_1
    newBook.position_book_up_long_2 =        data.position_book_up_long_2
    newBook.position_book_down_long_2 =        data.position_book_down_long_2
    newBook.position_book_up_long_3 =        data.position_book_up_long_3
    newBook.position_book_down_long_3 =        data.position_book_down_long_3
    newBook.position_book_up_long_4 =        data.position_book_up_long_4
    newBook.position_book_down_long_4 =        data.position_book_down_long_4
    newBook.position_book_up_long_5 =        data.position_book_up_long_5
    newBook.position_book_down_long_5 =        data.position_book_down_long_5
    newBook.position_book_up_long_6 =        data.position_book_up_long_6
    newBook.position_book_down_long_6 =        data.position_book_down_long_6
    newBook.position_book_up_long_7 =        data.position_book_up_long_7
    newBook.position_book_down_long_7 =        data.position_book_down_long_7
    newBook.position_book_up_long_8 =        data.position_book_up_long_8
    newBook.position_book_down_long_8 =        data.position_book_down_long_8
    newBook.position_book_up_long_9 =        data.position_book_up_long_9
    newBook.position_book_down_long_9 =        data.position_book_down_long_9
    newBook.position_book_up_long_10 =        data.position_book_up_long_10
    newBook.position_book_down_long_10 =        data.position_book_down_long_10
    newBook.position_book_up_long_20 =        data.position_book_up_long_20
    newBook.position_book_down_long_20 =        data.position_book_down_long_20
    newBook.position_book_up_long_40 =        data.position_book_up_long_40
    newBook.position_book_down_long_40 =        data.position_book_down_long_40
    newBook.position_book_up_long_60 =        data.position_book_up_long_60
    newBook.position_book_down_long_60 =        data.position_book_down_long_60
    newBook.position_book_up_long_80 =        data.position_book_up_long_80
    newBook.position_book_down_long_80 =        data.position_book_down_long_80
    newBook.position_book_up_long_100 =        data.position_book_up_long_100
    newBook.position_book_down_long_100 =        data.position_book_down_long_100

    dbSaveBook.add(newBook)
    dbSaveBook.commit()
