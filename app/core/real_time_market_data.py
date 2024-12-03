import asyncio
import MetaTrader5 as mt5

class RealTimeMarketData:
    def __init__(self):
        self.mt5 = mt5

    async def get_real_time_data(self, symbol):
        while True:
            try:
                price = await self.get_current_price(symbol)
                yield price
            except Exception as e:
                print(f"Error fetching data: {e}")
                await asyncio.sleep(1)

    async def get_current_price(self, symbol):
        tick = self.mt5.symbol_info_tick(symbol)
        print(f"Data: {tick}")
        return tick.ask  # Return the ask price

async def real_time_market_data(symbol):
    market_data = RealTimeMarketData()
    async for price in market_data.get_real_time_data(symbol):
        yield price
