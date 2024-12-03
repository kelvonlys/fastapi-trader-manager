import asyncio
import MetaTrader5 as mt5

class RealTimeMarketData:
    def __init__(self):
        self.mt5 = mt5

    async def get_real_time_data(self, symbol, interval_seconds=1):
        while True:
            try:
                tick = await self.get_current_price(symbol)
                if tick:  # Check if tick is valid
                    yield {
                        'time': tick.time,
                        'bid': tick.bid,
                        'ask': tick.ask,
                        'last': tick.last,
                        'volume': tick.volume,
                        'time_msc': tick.time_msc,
                        'flags': tick.flags,
                        'volume_real': tick.volume_real
                    }
                else:
                    raise ValueError(f"No tick data available for symbol: {symbol}")
            except Exception as e:
                print(f"Error fetching data: {e}")
                await asyncio.sleep(1)
            await asyncio.sleep(interval_seconds)

    async def get_current_price(self, symbol):
        tick = self.mt5.symbol_info_tick(symbol)
        if tick:
            print(f"Data: {tick}")
            return tick  # Return the complete tick object
        else:
            return None  # Return None if no tick data is available

async def real_time_market_data(symbol):
    market_data = RealTimeMarketData()
    async for price in market_data.get_real_time_data(symbol):
        yield price
