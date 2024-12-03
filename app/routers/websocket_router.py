from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core import real_time_market_data
from app.core.websocket_manager import websocket_manager
import asyncio

router = APIRouter()

@router.websocket("/ws/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    try:
        await websocket.accept()
        
        # Register the connection with WebSocketManager
        await websocket_manager.register(websocket)
        
        try:
            market_data = real_time_market_data.real_time_market_data(symbol)
            async for price in market_data:
                if websocket_manager.connections:
                    await websocket.send_json({'type': 'price', 'data': price})
                
                # Check if any connections exist
                if not websocket_manager.connections:
                    raise WebSocketDisconnect("No active connections")
                
                # Check heartbeat every minute
                # if not await websocket_manager.check_heartbeat(websocket):
                    # raise WebSocketDisconnect("Heartbeat failed")
        finally:
            # Unregister the connection with WebSocketManager
            await websocket_manager.unregister(websocket)
    except WebSocketDisconnect:
        pass
    finally:
        # Close all connections after unregistration
        asyncio.create_task(websocket_manager.close_all_connections())