import asyncio
import MetaTrader5 as mt5

class RealTimeMarketData:
    def __init__(self):
        self.mt5 = mt5
        self.previous_bid = None
        self.previous_ask = None

    async def get_real_time_data(self, symbol, interval_seconds=1):
        while True:
            try:
                symbol_info = await self.get_current_info(symbol)
                if symbol_info:
                    current_bid = round(symbol_info.bid, 4) 
                    current_ask = round(symbol_info.ask, 4)
                    current_spread = round(symbol_info.spread, 4)
                   # current_spread = symbol_info.spread
                    day_change_pct = symbol_info.price_change
                    
                    # Limit day_change_pct to 4 decimal places 
                    day_change_pct = round(day_change_pct, 4)

                    data = {
                        'time': symbol_info.time,
                        'bid': current_bid,
                        'ask': current_ask,
                        'last': symbol_info.last,
                        'volume': symbol_info.volume,
                        'volume_real': symbol_info.volume_real,
                        'day_change_pct': day_change_pct,
                        'spread': current_spread,
                        'previous_bid': self.previous_bid,
                        'previous_ask': self.previous_ask,
                        
                    }

                    # Update previous_bid and previous_ask
                    self.previous_bid = current_bid
                    self.previous_ask = current_ask
                    
                    print(f"Data: {data}")

                    yield data
                else:
                    raise ValueError(f"No data available for symbol: {symbol}")
            except Exception as e:
                print(f"Error fetching data: {e}")
                await asyncio.sleep(1)
            await asyncio.sleep(interval_seconds)

    async def get_current_info(self, symbol):
        symbol_info = self.mt5.symbol_info(symbol)
        if symbol_info:
            #print(f"Data: {symbol_info}")
            return symbol_info
        else:
            return None

async def real_time_market_data(symbol):
    market_data = RealTimeMarketData()
    async for price in market_data.get_real_time_data(symbol):
        yield price
