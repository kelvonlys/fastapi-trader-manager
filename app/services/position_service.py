from typing import List, Dict, Any
from fastapi import HTTPException
import MetaTrader5 as mt5
import json

class PositionService:
    def __init__(self):
        self.positions = []

    import json

    def get_open_positions(self):
        # Get all current positions
        self.positions = mt5.positions_get()
        
        if self.positions:
            # Initialize an empty list to store all position data
            all_positions_data = []
            
            # Iterate over each position
            for position in self.positions:
                # Create a dictionary with the required information for this position
                position_data = {
                    'position_id': position.ticket,
                    'symbol': position.symbol,
                    'price': position.price_current,
                    'stop_loss': position.sl,
                    'profit': position.profit,
                    'volume': position.volume,
                    'time': position.time,
                    'type': position.type
                }
                
                # Add this position's data to the list
                all_positions_data.append(position_data)
                print(f"Position data: {position_data}")
            
            # Convert the list of dictionaries to JSON
            positions_json = json.dumps(all_positions_data)
            
            return positions_json
        else:
            return "No open positions"

    def modify_position(self, position_id: int) -> Dict[str, Any]:
        for pos in self.positions:
            if pos["id"] == position_id:
                # Modify the position data
                pos["price"] = mt5.symbol_info_tick(pos["symbol"]).price
                pos["sl"] = mt5.symbol_info_tick(pos["symbol"]).bid - 20  # Example stop loss adjustment
                pos["tp"] = mt5.symbol_info_tick(pos["symbol"]).ask + 20  # Example take profit adjustment
                
                return pos
        raise HTTPException(status_code=404, detail="Position not found")

 
