import os 
from dotenv import load_dotenv 
from fastapi import FastAPI
from app.core import mt5_integration, market_data
from app.routers import orders, positions

load_dotenv()
app = FastAPI()
@app.get("/") 

async def read_root():    
    return {"Hello": "World"}

# Initialize MT5 connection
mt5 = mt5_integration.MT5Integration()

# Initialize market data service
#market_data_service = market_data.MarketDataService()

# Include router modules
app.include_router(orders.router)
app.include_router(positions.router)
