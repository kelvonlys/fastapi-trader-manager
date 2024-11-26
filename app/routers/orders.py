from fastapi import APIRouter
from app.services.order_service import OrderService

router = APIRouter()

@router.post("/create")
async def create_order(order: dict):
    order_service = OrderService()
    return order_service.create_order(order)

@router.get("/list")
async def list_orders():
    order_service = OrderService()
    return order_service.list_orders()
