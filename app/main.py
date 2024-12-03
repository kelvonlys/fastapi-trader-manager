import os 
from dotenv import load_dotenv 
from fastapi import FastAPI
from app.core import mt5_integration, real_time_market_data
from app.routers import orders, positions
from fastapi import WebSocket

load_dotenv()
app = FastAPI()
@app.get("/") 

async def read_root():    
    return {"Hello": "World"}

# Initialize MT5 connection
mt5 = mt5_integration.MT5Integration()

# Include router modules
app.include_router(orders.router)
app.include_router(positions.router)

@app.websocket("/ws/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()
    
    try:
        async for price in real_time_market_data.real_time_market_data(symbol):
            await websocket.send_json({'type': 'price', 'data': price})
    except Exception as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
