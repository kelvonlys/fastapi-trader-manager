from typing import List, Dict, Any
from fastapi import HTTPException
import MetaTrader5 as mt5
import json

class PositionService:
    def __init__(self):
        self.positions = []

    def get_open_positions(self):
        # Get the current position  
        self.positions = mt5.positions_get()
        if self.positions:
            current_position = self.positions[0]  # Assuming only one position
            print(f"Current position: {current_position}")
            
            # Get the symbol info
            symbol_info = mt5.symbol_info(current_position.symbol) if current_position else None

            # Get the symbol info tick (current price)
            symbol_tick = mt5.symbol_info_tick(current_position.symbol) if current_position else None

            # Create a dictionary with the required information
            position_data = {
                'position_id': current_position.ticket if current_position else None,
                'symbol': current_position.symbol if current_position else None,
                #'price': current_position.price_current if current_position else None,
                'stop_loss': current_position.sl if current_position else None,
                'profit': current_position.profit if current_position else None,
                'volume': current_position.volume if current_position else None,
                'time': current_position.time if current_position else None,
                'type': current_position.type if current_position else None
            }
            
            print(f"Position data: {position_data}")

            # Convert the dictionary to JSON
            position_json = json.dumps(position_data)
            
            return position_json
            print(position_json)

    def modify_position(self, position_id: int) -> Dict[str, Any]:
        for pos in self.positions:
            if pos["id"] == position_id:
                self.positions.remove(pos)
                return pos
        raise HTTPException(status_code=404, detail="Position not found")

 
