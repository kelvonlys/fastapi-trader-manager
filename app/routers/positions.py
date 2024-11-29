from fastapi import APIRouter
from app.services.position_service import PositionService

router = APIRouter()

position_service = PositionService()

@router.get("/open-positions")
async def get_open_positions():
    return position_service.get_open_positions()

@router.post("/open-position")
async def open_position(position: dict):
    return position_service.open_position(position)

@router.put("/modify-position/{position_id}")
async def modify_position(position_id: int):
    return position_service.modify_position(position_id)
