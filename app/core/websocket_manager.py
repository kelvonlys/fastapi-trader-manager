import time
import asyncio
from fastapi import WebSocket, WebSocketDisconnect

class WebSocketManager:
    def __init__(self):
        self.connections = {}
        self.timeout_period = 300  # 5 minutes in seconds
        # Start the periodic cleanup task
        print("Starting periodic cleanup task")
        asyncio.create_task(self.periodic_cleanup())
        # Start periodic heartbeat checks
        asyncio.create_task(self.periodic_heartbeat_check())

    async def register(self, websocket: WebSocket):
        client_id = f"{websocket.client[0]}:{websocket.client[1]}"
        print(f"Registering connection: {client_id}")
        self.connections[client_id] = {
            'websocket': websocket,
            'last_activity': time.time(),
            'heartbeat_interval': None
        }
        # Start the heartbeat if it's not already running
        if not self.connections[client_id]['heartbeat_interval']:
            await self.start_heartbeat(websocket)

    async def unregister(self, websocket: WebSocket):
        client_id = f"{websocket.client[0]}:{websocket.client[1]}"
        if client_id in self.connections:
            print(f"Unregistering connection: {client_id}")
            if self.connections[client_id]['heartbeat_interval']:
                self.connections[client_id]['heartbeat_interval'].cancel()
            del self.connections[client_id]

    async def close_all_connections(self):
        print("Closing all connections")
        for conn_id, conn_data in list(self.connections.items()):
            await conn_data['websocket'].close()
            del self.connections[conn_id]

    async def start_heartbeat(self, websocket: WebSocket):
        client_id = f"{websocket.client[0]}:{websocket.client[1]}"
        print(f"Starting heartbeat for connection: {client_id}")
        heartbeat_interval = 30  # Send heartbeat every 30 seconds
        self.connections[client_id]['heartbeat_interval'] = asyncio.create_task(
            self.send_heartbeat(websocket, client_id, heartbeat_interval)
        )

    async def send_heartbeat(self, websocket: WebSocket, client_id, interval):
        while client_id in self.connections and not websocket.client_state == 3:
            try:
                print(f"Sending heartbeat to connection: {client_id}")
                await websocket.send_json({'type': 'heartbeat'})
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error sending heartbeat to {client_id}: {e}")
                break
        print(f"Stopped heartbeat for connection: {client_id}")

    async def check_heartbeat(self, websocket: WebSocket):
        client_id = f"{websocket.client[0]}:{websocket.client[1]}"
        print(f"Checking heartbeat for connection: {client_id}")
        if client_id in self.connections:
            last_heartbeat = self.connections[client_id]['last_activity']
            current_time = time.time()
            if current_time - last_heartbeat > 60:  # If no heartbeat in 60 seconds
                print(f"Heartbeat failed for connection: {client_id}")
                return False
            else:
                self.connections[client_id]['last_activity'] = current_time
                return True
        return False

    async def periodic_cleanup(self):
        while True:
            print("Running periodic cleanup")
            current_time = time.time()
            expired_connections = [
                conn_id for conn_id, conn_data in self.connections.items()
                if current_time - conn_data['last_activity'] > self.timeout_period
            ]
            
            for conn_id in expired_connections:
                print(f"Closing expired connection: {conn_id}")
                await self.connections[conn_id]['websocket'].close()
                del self.connections[conn_id]
            
            await asyncio.sleep(600)  # Check every minute

    async def periodic_heartbeat_check(self):
        while True:
            print("Running periodic heartbeat check")
            for conn_id, conn_data in self.connections.items():
                websocket = conn_data['websocket']
                if not await self.check_heartbeat(websocket):
                    await self.unregister(websocket)
            await asyncio.sleep(60)  # Check heartbeats every minute

websocket_manager = WebSocketManager()
